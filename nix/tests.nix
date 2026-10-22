{ pkgs, website, devShell, websiteApp }:

{
  # Smoke test the built website by serving it with Python HTTP server
  test-smoke = pkgs.runCommand "test-smoke"
    {
      inherit website;
      nativeBuildInputs = [ pkgs.python3 pkgs.curl ];
    }
    ''
      echo "Starting Python HTTP server for smoke tests..."

      PORT=8765
      python3 -m http.server $PORT --directory "${website}" &
      SERVER_PID=$!

      # Wait for server to be ready (up to 10 seconds)
      for i in $(seq 1 20); do
        if curl -s -o /dev/null "http://127.0.0.1:$PORT/"; then
          echo "✅ Server is ready"
          break
        fi
        sleep 0.5
        if [ "$i" = "20" ]; then
          echo "❌ Server failed to start in time"
          kill $SERVER_PID 2>/dev/null
          exit 1
        fi
      done

      FAILED=0

      check_content() {
        local path="$1"
        local expected="$2"
        local description="$3"

        if curl -s "http://127.0.0.1:$PORT$path" | grep -q "$expected"; then
          echo "✅ $description"
        else
          echo "❌ $description (expected to find: \"$expected\" at $path)"
          FAILED=1
        fi
      }

      check_status() {
        local path="$1"
        local expected_code="$2"
        local description="$3"

        actual=$(curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:$PORT$path")
        if [ "$actual" = "$expected_code" ]; then
          echo "✅ $description (HTTP $actual)"
        else
          echo "❌ $description (expected HTTP $expected_code, got HTTP $actual)"
          FAILED=1
        fi
      }

      # Homepage
      check_status "/" "200" "Homepage returns HTTP 200"
      check_content "/" "QGIS.org Blog" "Homepage has site title"
      check_content "/" "Official news and announcements from the QGIS project." "Homepage has subtitle"
      check_content "/" "QGIS sustaining members" "Homepage has sustaining members section"

      # Author pages
      check_status "/author/underdark/" "200" "Author page (Anita Graser) returns HTTP 200"
      check_content "/author/underdark/" "Anita Graser" "Author page has author name"

      # Category pages
      check_status "/category/qgis-release-announcements/" "200" "Category page returns HTTP 200"
      check_content "/category/qgis-release-announcements/" "QGIS Release Announcements" "Category page has expected heading"

      # 404 handling
      check_status "/this-page-does-not-exist/" "404" "Non-existent path returns HTTP 404"

      kill $SERVER_PID 2>/dev/null
      wait $SERVER_PID 2>/dev/null || true

      if [ "$FAILED" = "1" ]; then
        echo ""
        echo "❌ Smoke tests FAILED"
        exit 1
      fi

      echo ""
      echo "✅ All smoke tests passed"
      echo "Smoke tests passed" > $out
    '';

  # Test dev shell has required tools
  test-dev-shell = pkgs.runCommand "test-dev-shell"
    {
      nativeBuildInputs = devShell.nativeBuildInputs or [ ]
        ++ devShell.buildInputs or [ ];
    }
    ''
      echo "Testing dev shell tools..."

      # Check hugo is available
      if ! command -v hugo &> /dev/null; then
        echo "❌ hugo not found in dev shell"
        exit 1
      fi

      echo "✅ hugo available: $(hugo version)"

      # Check python is available
      if ! command -v python3 &> /dev/null; then
        echo "❌ python3 not found in dev shell"
        exit 1
      fi

      echo "✅ python3 available: $(python3 --version)"

      # Check make is available
      if ! command -v make &> /dev/null; then
        echo "❌ make not found in dev shell"
        exit 1
      fi

      echo "✅ make available: $(make --version | head -1)"

      echo "Dev shell verification passed" > $out
    '';

  # Unit tests for the WordPress-to-Bulma markup transform, plus the corpus
  # guard tests that enforce the golden rule: media and page link structures
  # must survive the transform unchanged.
  test-wp-to-bulma = pkgs.runCommand "test-wp-to-bulma"
    {
      nativeBuildInputs = [ pkgs.python3 ];
      scriptsSrc = ../scripts;
      postsSrc = ../content/posts;
    }
    ''
      echo "Running WordPress-to-Bulma transform tests..."

      # The guard tests read the real post corpus, so both trees are copied in.
      cp -r "$scriptsSrc" scripts
      cp -r "$postsSrc" posts
      chmod -R u+w scripts posts

      export WP_CORPUS="$PWD/posts"

      if ! python3 -m unittest discover -s scripts/tests -t . -v; then
        echo "❌ WordPress-to-Bulma tests FAILED"
        exit 1
      fi

      echo ""
      echo "✅ WordPress-to-Bulma tests passed"
      echo "wp_to_bulma tests passed" > $out
    '';

  # Package builds successfully (implicit check)
  build-website = website;
}
