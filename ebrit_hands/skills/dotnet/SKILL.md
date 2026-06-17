---
description: .NET 9 SDK enabled — pre-installed tools, build and test commands for C#/.NET projects.
name: dotnet
triggers:
- dotnet
- .NET
- csproj
- nuget
- sln
---

# Environment description:

This environment has **.NET 9 SDK** pre-installed at `/usr/local/dotnet`.

## dotnet is already on PATH

No installation needed. Verify with:

```bash
dotnet --version
dotnet --list-sdks
```

## Building and testing

```bash
dotnet restore
dotnet build --no-restore
dotnet test --no-build --logger "console;verbosity=normal"
```

## Useful flags

```bash
dotnet build -c Release
dotnet test --filter "FullyQualifiedName~MyTest"
dotnet publish -c Release -o ./out
```

## NuGet / private feeds

If `dotnet restore` fails due to a private feed, check `NuGet.config` in the repo root — credentials may be required. Ask the user before proceeding.

## Notes

- Run as user `openhands` (non-root). `sudo` is available if needed.
- Do **not** run `dotnet-install.sh` again — SDK is already present.
- `DOTNET_CLI_TELEMETRY_OPTOUT=1` and `DOTNET_NOLOGO=1` are recommended for non-interactive runs.
