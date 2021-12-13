.DEFAULT_GOAL:=help

pretty:  ## Run prettier against our source code
	prettier index.html --write

serve:  ## Serve the current directory with Python
	python3 -m http.server 8000 --bind 127.0.0.1

.PHONY: pretty serve

help:  ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
