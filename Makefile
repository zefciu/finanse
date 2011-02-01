all:
	mkdir static
	# ln -s css static/css
	mkdir static/extjs
	@echo Deploy EXTJS to static/extjs
	mkdir static/js
	java -jar compiler.jar --js js/index.js --js_output_file static/js/index.js 
	ln -s web.py init.wsgi

clean:
	rm -r static
	rm init.wsgi
