{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-24.05"; # or "unstable"
  
  # Use https://search.nixos.org/packages to find packages
  packages = [
    pkgs.docker
    pkgs.docker-compose
  ];
  
  # Sets environment variables in the workspace
  env = {};
  services.docker.enable = true;
  
  idx = {
    # Search for the extensions you want on https://open-vsx.org/ and use "publisher.id"
    extensions = [
      "ms-azuretools.vscode-docker"
    ];
    
    workspace = {
      # Runs when a workspace is first created with this `dev.nix` file
      onCreate = {
        setup-docker-compose = ''
          # Ensure Docker Compose is built only once
          docker-compose -f docker-compose.local.yml build
        '';
        # Open editors for the following files by default, if they exist:
        default.openFiles = ["docker-compose.local.yml"];
      };
      # To run something each time the workspace is (re)started, use the `onStart` hook
      onStart = {
        start-docker-compose = ''
          docker-compose -f docker-compose.local.yml up
        '';
      };
    };
    
    # Enable previews and customize configuration
    previews = {
      enable = true;
      previews = {
        web = {
          command = ["docker-compose" "-f" "docker-compose.local.yml" "up"];
          env = {
            PORT = "$PORT";
          };
          manager = "web";
        };
      };
    };
  };
}
