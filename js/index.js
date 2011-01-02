var Ext;

Ext.ns('Ext.fi', 'Ext.fi.nz')

Ext.fi.nz.onAdd = function (btn, ev) {
	var vals, rec;
	vals = Ext.fi.nz.form.getForm().getValues();
	rec = new Ext.fi.nz.store.recordType(vals);
	Ext.fi.nz.store.add(rec);
	Ext.fi.nz.form.getForm().reset();
};

Ext.fi.nz.CommonCombo = Ext.extend(Ext.form.ComboBox, {
		initComponent: function () {
			this.store = new Ext.data.JsonStore({
					url: this.url,
					fields: ['id', 'nazwa'],
					restful: true
				});
			Ext.fi.nz.CommonCombo.superclass.initComponent.apply(
				this, arguments
			);
		},
		valueField: 'id',
		displayField: 'nazwa',
		mode: 'remote',
		triggerAction: 'all',
		submitValue: true
	});

Ext.fi.nz.form = new Ext.form.FormPanel({
		region: 'west',
		width: 500,
		items: [
			Ext.fi.nz.cat_combo = new Ext.fi.nz.CommonCombo({
					url: 'kategorie',
					fieldLabel: 'Kategoria',
					name: 'kategoria.nazwa',
					hiddenName: 'kategoria.id'
				}),
			Ext.fi.nz.subcat_combo = new Ext.fi.nz.CommonCombo({
					fieldLabel: 'Podkategoria',
					url: 'podkategorie',
					name: 'podkategoria.nazwa',
					hiddenName: 'podkategoria.id'
				}),
			Ext.fi.nz.product_combo = new Ext.fi.nz.CommonCombo({
					fieldLabel: 'Produkt',
					url: 'produkty',
					name: 'produkt.nazwa',
					hiddenName: 'produkt.id'
				}),
			new Ext.form.TextField({name: 'ilosc', fieldLabel: 'Ilość'}),
			new Ext.form.TextField({name: 'cena', fieldLabel: 'Cena'})
		], buttons: [
			{
				text: 'Dodaj',
				handler: Ext.fi.nz.onAdd
			}
		]
	});


Ext.fi.nz.store = new Ext.data.JsonStore({
		url: 'zakupy',
		autoSave: false,
		restful: true,
		fields: [
			'id', 'produkt.id', 'produkt.nazwa', 'kategoria.id',
			'kategoria.nazwa', 'podkategoria.id', 'podkategoria.nazwa', 'cena',
			'ilosc' ],
		writer: new Ext.data.JsonWriter()
	});

Ext.fi.nz.store.on('beforesave', function (store, data) {
		console.log(data.create);
});

Ext.fi.nz.onSubmit = function () {
	Ext.fi.nz.store.save();
}


Ext.fi.nz.grid = new Ext.grid.GridPanel({
		region: 'center',
		store: Ext.fi.nz.store,
		columns: [
			{header: 'Kategoria', dataIndex: 'kategoria.nazwa'},
			{header: 'Podkategoria', dataIndex: 'podkategoria.nazwa'},
			{header: 'Produkt', dataIndex: 'produkt.nazwa'},
			{header: 'Ilość', dataIndex: 'ilosc'},
			{header: 'Cena', dataIndex: 'cena'},
		],
		tbar: [
			new Ext.form.Label({text: 'Sklep:'}),
			Ext.fi.nz.shop_combo = new Ext.fi.nz.CommonCombo({
					url: 'sklepy'
				}),
			new Ext.form.Label({text: 'Data:'}),
			Ext.fi.nz.date_field = new Ext.form.DateField({format: 'Y-m-d'})
		],
		bbar: [
			{
				text: 'Zapisz zakupy',
				handler: Ext.fi.nz.onSubmit
			}
		]
	});

Ext.onReady(function () {
		Ext.fi.nz.vp = new Ext.Viewport({
				layout: 'border',
				items: [Ext.fi.nz.form, Ext.fi.nz.grid]
			});
		Ext.fi.nz.cat_combo.on('select', function (combo, rec, i) {
				Ext.fi.nz.subcat_combo.store.setBaseParam(
					'kategoria_id', rec.get('id')
				);
				Ext.fi.nz.subcat_combo.store.load();
			});
		Ext.fi.nz.subcat_combo.on('select', function (combo, rec, i) {
				Ext.fi.nz.product_combo.store.setBaseParam(
					'podkategoria_id', rec.get('id')
				);
				Ext.fi.nz.product_combo.store.load();
			});
	});
