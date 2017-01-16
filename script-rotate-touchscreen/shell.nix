let pkgs = import <nixpkgs> {};
in with pkgs; let
    devDependencies = [
    ];

    dependencies = [
      python3
    ];
in {
    devEnv = stdenv.mkDerivation {
        name = "python3-dev-env";
        buildInputs = devDependencies ++ dependencies;
    };
}

