#define MyAppName "DietaryIndex"
#ifndef AppVersion
  #define AppVersion "0.3.0"
#endif
#ifndef ProjectRoot
  #define ProjectRoot "..\.."
#endif
#define DistDir ProjectRoot + "\electron_app\out\DietaryIndex-win32-x64"

[Setup]
AppId={{6F3C7868-2D7D-4C93-81C5-5E2C9877A18D}
AppName={#MyAppName}
AppVersion={#AppVersion}
AppPublisher=DietaryIndex
DefaultDirName={localappdata}\Programs\DietaryIndex
DefaultGroupName=DietaryIndex
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
LicenseFile={#ProjectRoot}\LICENSE
OutputDir={#ProjectRoot}\dist\installer
OutputBaseFilename=DietaryIndexElectronSetup-{#AppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\DietaryIndex.exe
CloseApplications=yes
RestartApplications=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "chinesesimplified"; MessagesFile: "Languages\ChineseSimplified.isl"

[CustomMessages]
english.LaunchDietaryIndex=Launch DietaryIndex
chinesesimplified.LaunchDietaryIndex=启动 DietaryIndex
english.ConfiguringMcp=Configuring Codex MCP...
chinesesimplified.ConfiguringMcp=正在配置 Codex MCP...
english.ConfigureMcp=Configure DietaryIndex MCP
chinesesimplified.ConfigureMcp=配置 DietaryIndex MCP

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "{#DistDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#ProjectRoot}\dist\DietaryIndexMCP.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#ProjectRoot}\packaging\windows\register_codex_mcp.ps1"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\DietaryIndex"; Filename: "{app}\DietaryIndex.exe"
Name: "{group}\卸载 DietaryIndex"; Filename: "{uninstallexe}"
Name: "{group}\{cm:ConfigureMcp}"; Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; Parameters: "-NoProfile -ExecutionPolicy Bypass -File ""{app}\register_codex_mcp.ps1"""; WorkingDir: "{app}"
Name: "{autodesktop}\DietaryIndex"; Filename: "{app}\DietaryIndex.exe"; Tasks: desktopicon

[Run]
Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; Parameters: "-NoProfile -ExecutionPolicy Bypass -File ""{app}\register_codex_mcp.ps1"""; StatusMsg: "{cm:ConfiguringMcp}"; Flags: postinstall skipifsilent runhidden
Filename: "{app}\DietaryIndex.exe"; Description: "{cm:LaunchDietaryIndex}"; Flags: nowait postinstall skipifsilent

[UninstallRun]
Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; Parameters: "-NoProfile -ExecutionPolicy Bypass -File ""{app}\register_codex_mcp.ps1"" -Unregister"; RunOnceId: "RemoveDietaryIndexMcp"; Flags: runhidden
