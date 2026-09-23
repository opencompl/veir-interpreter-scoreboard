{
  description = "VeIR interpreter scoreboard";

  inputs = {
    veir.url = "github:opencompl/veir";
    nixpkgs.follows = "veir/nixpkgs";
  };

  outputs = { self, nixpkgs, veir }:
    let
      currentVeir = (builtins.fromJSON (builtins.readFile ./flake.lock)).nodes.veir.locked;
      systems = [
        "aarch64-darwin"
        "aarch64-linux"
        "x86_64-darwin"
        "x86_64-linux"
      ];
      forAllSystems = nixpkgs.lib.genAttrs systems;
    in
    {
      packages = forAllSystems (system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in
        {
          clone-veir = pkgs.writeShellApplication {
            name = "get-upstream-veir";
            runtimeInputs = [ pkgs.git ];
            text = ''
              destination="''${1:-veir}"

              if [ "$#" -gt 1 ]; then
                echo "usage: get-upstream-veir [destination]" >&2
                exit 2
              fi

              if [ -e "$destination" ]; then
                if ! git -C "$destination" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
                  echo "destination is not a Git working tree: $destination" >&2
                  exit 1
                fi
              else
                git clone --no-checkout \
                  -- \
                  "https://github.com/${currentVeir.owner}/${currentVeir.repo}.git" \
                  "$destination"
              fi

              git -C "$destination" fetch --depth 1 origin ${currentVeir.rev}
              git -C "$destination" checkout --detach FETCH_HEAD
            '';
          };
        });

      devShells = forAllSystems (system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in
        {
          # Keep the development environment exactly aligned with VeIR's
          # pinned compiler, MLIR, and Lean toolchain.
          default = pkgs.mkShell {
            inputsFrom = [ veir.devShells.${system}.default ];
            packages = [
              self.packages.${system}.clone-veir
              pkgs.uv
            ];
          };
        });
    };
}
