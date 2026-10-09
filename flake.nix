{
  description = "Python 3.14 + Flet Dev Shell";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";
  };

  outputs = {
    self,
    nixpkgs,
  }: let
    system = "x86_64-linux";
    pkgs = import nixpkgs {inherit system;};

    # Bibliotecas C/GTK necessárias pelo runtime do Flet no Linux
    runtimeLibs = with pkgs; [
      gtk3
      glib
      gdk-pixbuf
      pango
      cairo
      atk
      harfbuzz
      libGL
      libepoxy
      libx11
      libxcursor
      libxrandr
      libxi
      mpv-unwrapped
      libsecret
      fontconfig
    ];
  in {
    devShells.${system}.default = pkgs.mkShell {
      buildInputs = with pkgs;
        [
          python314
          uv
        ]
        ++ runtimeLibs;

      shellHook = ''
        export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath runtimeLibs}:$LD_LIBRARY_PATH"
      '';
    };
  };
}
