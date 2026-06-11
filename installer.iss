; File: installer.iss
; Inno Setup installer for TaskSorter AI
;
; Produces: TaskSorterInstaller.exe
; Build command:
;   iscc installer.iss
;
; The installer:
;   1. Installs TaskSorter.exe and supporting files
;   2. Installs Ollama (AI backend via bundled OllamaSetup.exe)
;   3. Detects Ollama installation using full paths (not stale PATH)
;   4. Starts Ollama server if not already running
;   5. Waits until the Ollama server is actually accepting connections
;   6. Downloads the gemma3:1b AI model
;   7. Creates Start Menu and Desktop shortcuts
;   8. Launches TaskSorter on completion


[Setup]
AppName=TaskSorter
AppVersion=1.0
DefaultDirName={autopf}\TaskSorter
DefaultGroupName=TaskSorter
OutputDir=output
OutputBaseFilename=TaskSorterInstaller
Compression=lzma
SolidCompression=yes
; CHANGE: Windows/Linux icon compatibility fix
SetupIconFile=assets\icon.ico
; CHANGE: Ollama detection fix - request admin privileges for elevation
PrivilegesRequired=admin


[Files]
; CHANGE: Windows/Linux icon compatibility fix
Source: "dist\TaskSorter.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "config.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "credentials.json"; DestDir: "{app}"; Flags: ignoreversion
; CHANGE: Installation timing fix - tasks.json is generated automatically by
; the application on first save (task_storage.load_tasks returns [] when
; the file is missing), so it does NOT need to be bundled in the installer.
Source: "OllamaSetup.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall


[Icons]
; CHANGE: Windows/Linux icon compatibility fix
Name: "{group}\TaskSorter"; Filename: "{app}\TaskSorter.exe"; IconFilename: "{app}\TaskSorter.exe"
; CHANGE: Windows/Linux icon compatibility fix
Name: "{commondesktop}\TaskSorter"; Filename: "{app}\TaskSorter.exe"; IconFilename: "{app}\TaskSorter.exe"


[UninstallRun]
; CHANGE: Ollama detection fix - stop Ollama server cleanly on uninstall
Filename: "{localappdata}\Programs\Ollama\ollama.exe"; \
    Parameters: "stop"; \
    Flags: runhidden skipifdoesntexist


[Run]

; ───────────────────────────────────────────────
; STEP 1: Install Ollama (bundled setup executable)
; ───────────────────────────────────────────────
; OllamaSetup.exe extracts Ollama to %LOCALAPPDATA%\Programs\Ollama\
; and adds that directory to the User PATH.
; The waituntilterminated flag blocks until the installer completes.
; CHANGE: Ollama detection fix - all subsequent Ollama commands use
; the full installation path (not the stale PATH environment variable)
; CHANGE: Installation timing fix - wait for Ollama installer to finish
Filename: "{tmp}\OllamaSetup.exe"; \
    Description: "Installing Ollama..."; \
    StatusMsg: "Installing Ollama AI engine..."; \
    Flags: waituntilterminated

; ───────────────────────────────────────────────
; STEP 2: Launch TaskSorter (post-install)
; ───────────────────────────────────────────────
; nowait: installer does NOT wait for TaskSorter to close
; postinstall: only runs after installation is fully complete
; skipifsilent: skipped during silent installations
Filename: "{app}\TaskSorter.exe"; \
    Description: "Launch TaskSorter"; \
    Flags: nowait postinstall skipifsilent


[Code]

// ──────────────────────────────────────────────────────────
// CHANGE: Ollama detection fix — complete rewrite
// ──────────────────────────────────────────────────────────
//
// ROOT CAUSE ANALYSIS
// ────────────────────
// 1. OllamaSetup.exe extracts to %LOCALAPPDATA%\Programs\Ollama\ollama.exe
//    and adds that directory to the User PATH environment variable.
//
// 2. The Inno Setup process inherited its environment block at LAUNCH,
//    BEFORE Ollama was installed.  Its copy of PATH does NOT contain
//    the Ollama directory.
//
// 3. The original [Run] entries used 'cmd.exe /C ollama ...' — the
//    spawned cmd.exe inherits the installer's stale PATH and cannot
//    find 'ollama'.  The commands fail silently.
//
// 4. After a SYSTEM REBOOT: a fresh process inherits the updated
//    system PATH (which now includes Ollama) → 'ollama' is found.
//
// 5. On a SECOND installer run: the installer's inherited PATH
//    already includes Ollama (from the first installation) → works.
//
// FIX OVERVIEW
// ────────────
// A) Locate ollama.exe by checking KNOWN INSTALLATION PATHS on disk
//    instead of relying on the stale PATH variable.
// B) Retry the search with 1-second delays (up to 600 seconds / 10 minutes).
//    The Ollama installer may still be finishing file operations,
//    antivirus may be scanning, or the disk may be slow.
// C) Verify the found executable actually works (--version).
// D) Check whether the Ollama server is already running (ollama list).
// E) If not running, start ollama serve in the background (ewNoWait).
// F) Poll ollama list every second until the server is ready (max 60 s).
// G) Only then pull the AI model.
// H) Use a simple counter-based loop for timeouts (no GetTickCount
//    or PChar — both are not officially supported in Inno Setup
//    Pascal Script and would cause compilation errors).
// I) Provide clear error messages and fall back gracefully.
// ──────────────────────────────────────────────────────────


// ─────────────────────────────────────────────
// CHANGE: Ollama detection fix
// Locate ollama.exe by checking known installation directories.
// This does NOT rely on PATH, so it works even though the installer's
// environment was captured before Ollama was installed.
//
// Search order:
//   1. %LOCALAPPDATA%\Programs\Ollama\ollama.exe  (standard path)
//   2. %PROGRAMFILES%\Ollama\ollama.exe           (fallback)
//   3. bare 'ollama.exe' (last-resort PATH lookup)
// ─────────────────────────────────────────────
function FindOllamaExe(): string;
var
  OllamaDir: string;
begin
  // Standard Ollama installation path since v0.x
  OllamaDir := ExpandConstant('{localappdata}\Programs\Ollama');
  if FileExists(OllamaDir + '\ollama.exe') then
  begin
    Result := OllamaDir + '\ollama.exe';
    Log('FindOllamaExe: found at ' + Result);
    Exit;
  end;

  // Alternative: installed to Program Files
  OllamaDir := ExpandConstant('{commonpf}\Ollama');
  if FileExists(OllamaDir + '\ollama.exe') then
  begin
    Result := OllamaDir + '\ollama.exe';
    Log('FindOllamaExe: found at ' + Result);
    Exit;
  end;

  // Last resort: let the system resolve via PATH
  Result := 'ollama.exe';
  Log('FindOllamaExe: not found in standard locations, using bare name');
end;


// ─────────────────────────────────────────────
// CHANGE: Ollama startup validation
// Verify that ollama.exe is actually runnable by executing --version.
// Returns True if the executable exists and responds correctly.
// ─────────────────────────────────────────────
function ValidateOllamaExe(const OllamaExe: string): Boolean;
var
  ResultCode: Integer;
begin
  if not FileExists(OllamaExe) then
  begin
    Log('ValidateOllamaExe: file does not exist - ' + OllamaExe);
    Result := False;
    Exit;
  end;

  if Exec(OllamaExe, '--version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) and (ResultCode = 0) then
  begin
    Log('ValidateOllamaExe: version check OK (exit code ' + IntToStr(ResultCode) + ')');
    Result := True;
  end
  else
  begin
    Log('ValidateOllamaExe: version check FAILED (exit code ' + IntToStr(ResultCode) + ')');
    Result := False;
  end;
end;


// ─────────────────────────────────────────────
// CHANGE: Ollama readiness check
// Check whether the Ollama server is running and accepting connections.
// 'ollama list' queries the local server at localhost:11434.
// Returns True if the server responds.
// ─────────────────────────────────────────────
function IsOllamaReady(const OllamaExe: string): Boolean;
var
  ResultCode: Integer;
begin
  // 'ollama list' exits 0 if the server is reachable
  Result := Exec(OllamaExe, 'list', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) and (ResultCode = 0);
  if Result then
    Log('IsOllamaReady: server is ready')
  else
    Log(Format('IsOllamaReady: server not ready (exit code %d)', [ResultCode]));
end;


// ─────────────────────────────────────────────
// CHANGE: Retry logic — find ollama.exe
// Retry FindOllamaExe in a loop with 1-second delays.
// The Ollama installer may still be finalizing file operations
// (antivirus scanning, slow disk, etc.).
//
// Uses a simple counter-based loop instead of GetTickCount, which
// is not officially supported in Inno Setup Pascal Script.
// ─────────────────────────────────────────────
function FindOllamaExeWithRetry(MaxAttempts: Integer): string;
var
  Attempt: Integer;
begin
  Result := '';

  for Attempt := 1 to MaxAttempts do
  begin
    Result := FindOllamaExe();

    if FileExists(Result) then
    begin
      Log(Format('FindOllamaExeWithRetry: found on attempt %d/%d', [Attempt, MaxAttempts]));
      Exit;
    end;

    if Attempt < MaxAttempts then
    begin
      Log(Format('FindOllamaExeWithRetry: attempt %d/%d failed, retrying in 1s...', [Attempt, MaxAttempts]));
      Sleep(1000);
    end;
  end;

  // All retries exhausted — return whatever FindOllamaExe returned last
  Log('FindOllamaExeWithRetry: all retries exhausted');
  Result := FindOllamaExe();
end;


// ─────────────────────────────────────────────
// CHANGE: Ollama readiness check — wait loop
// Poll IsOllamaReady every second until the server responds
// or the maximum number of attempts is reached.
//
// Uses a simple counter-based loop instead of GetTickCount, which
// is not officially supported in Inno Setup Pascal Script.
// ─────────────────────────────────────────────
function WaitForOllamaReady(const OllamaExe: string; MaxAttempts: Integer): Boolean;
var
  Attempt: Integer;
begin
  Result := False;

  Log(Format('WaitForOllamaReady: polling every 1s (max %d attempts)', [MaxAttempts]));

  for Attempt := 1 to MaxAttempts do
  begin
    if IsOllamaReady(OllamaExe) then
    begin
      Log(Format('WaitForOllamaReady: server is ready (attempt %d/%d)', [Attempt, MaxAttempts]));
      Result := True;
      Exit;
    end;

    Log(Format('WaitForOllamaReady: attempt %d/%d, waiting 1s...', [Attempt, MaxAttempts]));
    Sleep(1000);
  end;

  Log(Format('WaitForOllamaReady: TIMEOUT after %d attempts', [MaxAttempts]));
end;


// ─────────────────────────────────────────────
// CHANGE: Ollama detection fix — main setup routine
//
// Called from CurStepChanged(ssPostInstall) after the [Run] section
// has finished executing (including OllamaSetup.exe).
//
// Flow:
//   1. Find ollama.exe with retry  (full path, not PATH, up to 600 s)
//   2. Validate it runs  (--version check)
//   3. Check if server is already running
//   4. If not running, start ollama serve (background)
//   5. Wait for server to be ready (poll list, max 60 s)
//   6. Pull gemma3:1b model
//   7. Report success or failure
//
// NOTE: Environment refresh (WM_SETTINGCHANGE broadcast) was removed
// because it requires PChar and PostMessage, both of which are not
// officially supported in Inno Setup Pascal Script.  Since the installer
// uses full paths to ollama.exe and does not rely on PATH, environment
// refresh is not needed for the installer to function correctly.
// ─────────────────────────────────────────────
procedure SetupOllama();
var
  OllamaExe: string;
  ResultCode: Integer;
  ServerAlreadyRunning: Boolean;
begin
  Log('SetupOllama: starting post-install Ollama setup');

  // ── Step 1: Find ollama.exe (retry up to 600 seconds) ──
  // CHANGE: Retry logic
  // CHANGE: Ollama detection fix
  OllamaExe := FindOllamaExeWithRetry(600);
  Log('SetupOllama: resolved OllamaExe = ' + OllamaExe);

  if not FileExists(OllamaExe) then
  begin
    Log('SetupOllama: CRITICAL — ollama.exe not found after 600 seconds');
    MsgBox(
      'Ollama installation could not be verified.'#13#10 +
      'The installer may not have completed successfully.'#13#10#13#10 +
      'TaskSorter will use offline fallback mode'#13#10 +
      '(limited AI functionality).'#13#10#13#10 +
      'You can re-run this installer or install Ollama manually'#13#10 +
      'from https://ollama.com',
      mbError,
      MB_OK
    );
    Exit;
  end;

  // ── Step 2: Validate the executable ──────────────────
  // CHANGE: Ollama startup validation
  if not ValidateOllamaExe(OllamaExe) then
  begin
    Log('SetupOllama: ollama.exe found but does not respond to --version');
    MsgBox(
      'Ollama was found but could not be started.'#13#10 +
      'The installation may be corrupted.'#13#10#13#10 +
      'TaskSorter will use offline fallback mode.',
      mbError,
      MB_OK
    );
    Exit;
  end;

  // ── Step 3: Check if server is already running ──────
  // CHANGE: Ollama startup validation
  ServerAlreadyRunning := IsOllamaReady(OllamaExe);

  if not ServerAlreadyRunning then
  begin
    // ── Step 4: Start ollama serve in background ──────
    // CHANGE: Ollama startup validation
    // CHANGE: Installation timing fix
    Log('SetupOllama: starting ollama serve...');
    if Exec(OllamaExe, 'serve', '', SW_HIDE, ewNoWait, ResultCode) then
      Log('SetupOllama: ollama serve launched in background')
    else
      Log('SetupOllama: failed to launch ollama serve (exit ' + IntToStr(ResultCode) + ')');
  end
  else
  begin
    Log('SetupOllama: Ollama server is already running — skipping serve');
  end;

  // ── Step 5: Wait until server accepts connections ───
  // CHANGE: Ollama readiness check
  if not WaitForOllamaReady(OllamaExe, 60) then
  begin
    Log('SetupOllama: server did not become ready within 60 seconds');
    MsgBox(
      'Ollama server did not start within the expected time.'#13#10 +
      'The AI model cannot be downloaded automatically.'#13#10#13#10 +
      'You can start Ollama manually and run:'#13#10 +
      '  ollama pull gemma3:1b',
      mbError,
      MB_OK
    );
    Exit;
  end;

  // ── Step 6: Pull the AI model ───────────────────────
  // CHANGE: Ollama readiness check
  // CHANGE: Installation timing fix
  Log('SetupOllama: pulling gemma3:1b model (this may take several minutes)...');
  if Exec(OllamaExe, 'pull gemma3:1b', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then
  begin
    if ResultCode = 0 then
    begin
      Log('SetupOllama: model pulled successfully');
    end
    else
    begin
      Log(Format('SetupOllama: model pull exited with code %d', [ResultCode]));
      MsgBox(
        'AI model download exited with code ' + IntToStr(ResultCode) + '.'#13#10 +
        'You can run "ollama pull gemma3:1b" manually later.',
        mbError,
        MB_OK
      );
    end;
  end
  else
  begin
    Log('SetupOllama: failed to execute ollama pull');
    MsgBox(
      'Could not start the AI model download.'#13#10 +
      'You can run "ollama pull gemma3:1b" manually later.',
      mbError,
      MB_OK
    );
  end;

  Log('SetupOllama: complete');
end;


// ─────────────────────────────────────────────
// CHANGE: Installation timing fix
// Entry point called by Inno Setup after all [Run] entries complete.
//
// ssPostInstall fires after:
//   1. All files have been extracted  ([Files])
//   2. All [Run] entries have been processed
//
// This is the correct moment to set up Ollama because:
//   - OllamaSetup.exe (in [Run]) has finished installing Ollama
//   - The installer is still active (not yet finalized)
//   - We can safely use Exec() to run post-install tasks
// ─────────────────────────────────────────────
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    Log('CurStepChanged(ssPostInstall): starting Ollama setup');
    SetupOllama();
    Log('CurStepChanged(ssPostInstall): finished');
  end;
end;
