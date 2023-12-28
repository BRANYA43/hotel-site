MANAGER_PATH = "src/manage.py"

startapp:
	python $(MANAGER_PATH) startapp $(name)
	mv ./$(name) src/$(name)
	rm src/$(name)/tests.py
	mkdir src/$(name)/templates/ \
		  src/$(name)/static/ \
		  src/$(name)/tests/
	touch src/$(name)/templates/.gitkepp \
		  src/$(name)/static/.gitkeep \
		  src/$(name)/tests/__init__.py \
  		  src/$(name)/forms.py \
  		  src/$(name)/urls.py

make_migrations:
	python $(MANAGER_PATH) makemigrations $(app)

migrate:
	python $(MANAGER_PATH) migrate $(app)

run_tests:
	python $(MANAGER_PATH) test $(app)

run_func_tests:
	python $(MANAGER_PATH) test $(if $(path), functional_tests.$(path), functional_tests)