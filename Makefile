all: testshell

test_shell:
	docker compose run 3d_printer_monitor bash
