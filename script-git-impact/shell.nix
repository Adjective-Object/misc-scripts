let pkgs = import <nixpkgs> {};
in with pkgs; let
    devDependencies = [
      shellcheck
    ];

    dependencies = [
      bash
    ];
in {
    devEnv = stdenv.mkDerivation {
        name = "bash-dev-env";
        buildInputs = devDependencies ++ dependencies;
    };
}

