.DEFAULT_GOAL:=help

DATABASE_NAME=J_agis_pour_ma_santé.db

load:  ## Load a CSV file into a SQLite database for datasette
	csvs-to-sqlite \
		--table 'Articles' \
		--replace-tables \
		--primary-key 'Identifiant (ID) du nœud' \
		--extract-column 'Statut:Statuts:name' \
		--extract-column 'Auteur courrier:Auteurs:email' \
		--datetime 'Date de modification' \
		--datetime 'Date de mise à jour' \
		--datetime-format '%d/%m/%Y %H:%M:%S' \
		'$(csv-file)' $(DATABASE_NAME)

serve:  ## Run the datasette server against SQLite database
	datasette $(DATABASE_NAME)  --metadata metadata.yml --cors

.PHONY: load serve

help:  ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
