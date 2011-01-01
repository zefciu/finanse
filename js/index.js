var Ext;

Ext.ns('Ext.fi', 'Ext.fi.nz')

Ext.fi.nz.form = new Ext.form.FormPanel({
		region: 'west',
		width: 500,
		items: [
			new Ext.form.ComboBox({
					fieldLabel: 'Kategoria',
					store: new Ext.data.JsonStore({
							url: 'kategorie',
							fields: ['id', 'nazwa']
						}),
					valueField: 'id',
					displayField: 'nazwa',
					mode: 'remote',
					triggerAction: 'all'
				}),
			new Ext.form.TextField({name: 'ilosc', fieldLabel: 'Ilość'}),
			new Ext.form.TextField({name: 'cena', fieldLabel: 'Cena'})
		]
	});

Ext.fi.nz.store = new Ext.data.JsonStore({
		restful: true,
		fields: [
			'id', 'produkt.id', 'produkt.nazwa', 'kategoria.id',
			'kategoria.nazwa', 'podkategoria.id', 'podkategoria.nazwa', 'cena',
			'ilosc' ]
	});
Ext.fi.nz.grid = new Ext.grid.GridPanel({
		region: 'center',
		store: Ext.fi.nz.store,
		columns: [
			{header: 'Kategoria', dataIndex: 'kategoria.nazwa'},
			{header: 'Podkategoria', dataIndex: 'podkategoria.nazwa'},
			{header: 'Produkt', dataIndex: 'produkt.nazwa'},
			{header: 'Ilość', dataIndex: 'ilosc'},
			{header: 'Cena', dataIndex: 'cena'},
		]
	});

Ext.onReady(function () {
		Ext.fi.nz.vp = new Ext.Viewport({
				layout: 'border',
				items: [Ext.fi.nz.form, Ext.fi.nz.grid]
			})
	});
