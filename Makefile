all: testshell

build:
	docker compose build 3d_printer_monitor

test_shell:
	docker compose run 3d_printer_monitor bash
