all:
	mkdir static
	# ln -s css static/css
	mkdir static/extjs
	@echo Deploy EXTJS to static/extjs
	mkdir static/js
	java -jar compiler.jar --js js/index.js --js_output_file static/js/index.js 

clean:
	rm -r static
