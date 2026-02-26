Name:           gamescope-session-steamdeck
Version:        1
Release:        1
Summary:        Steam Gamescope Session
License:        GPL
Group:          System/Session
URL:            https://github.com/ValveSoftware/gamescope

Requires:       gamescope
Requires:       steam
Requires:       xrandr
Requires:       xinput
BuildArch:      noarch

%description
This package provides a Steam Game Mode session for OpenMandriva,
allowing users to launch Steam's Gamepad UI inside Gamescope as a
selectable session in SDDM or any X11 session manager.

%prep

%build

%install
install -Dm755 /dev/null %{buildroot}/usr/bin/gamescope-steam-session
cat > %{buildroot}/usr/bin/gamescope-steam-session << 'EOF'
#!/bin/bash
# rotate the x session with xrandr BEFORE launching gamescope to not confuse where screen center is
xrandr --output eDP-1 --rotate right
xinput set-prop "FTS3528:00 2808:1015" "Coordinate Transformation Matrix" 0 1 0 -1 0 1 0 0 1
# launch gamescope at native Steam Deck res with a delay to avoid race condition with gamescope unfortunately rotating takes a bit
sleep 2
exec /usr/bin/gamescope -W 1280 -H 800 --integer-scaling -f --steam -- steam -gamepadui
EOF

# Desktop session file
install -Dm644 /dev/null %{buildroot}/usr/share/xsessions/gamescope-steam.desktop
cat > %{buildroot}/usr/share/xsessions/gamescope-steam.desktop << 'EOF'
[Desktop Entry]
Name=Steam Game Mode (Gamescope)
Comment=Launch Steam Gamepad UI inside Gamescope
Exec=/usr/bin/gamescope-steam-session
Type=Application
DesktopNames=GamescopeSteam
EOF

%files
/usr/bin/gamescope-steam-session
/usr/share/xsessions/gamescope-steam.desktop
