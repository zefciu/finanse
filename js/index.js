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

Ext.fi.nz.CommonCF = Ext.extend(Ext.form.CompositeField, {
		initComponent: function () {
			this.items = [
				this.combo = new Ext.fi.nz.CommonCombo(this.comboConf),
				this.btn = new Ext.Button({
						text: 'Dodaj',
						handler: this.onAdd,
						scope: this
					})
			]
			Ext.fi.nz.CommonCF.superclass.initComponent.apply(this, arguments);
			this.relayEvents(this.combo, 'select');
		},
		onAdd: function () {
			Ext.Msg.prompt(
				this.fieldLabel + ' - dodawanie',
				'Podaj nazwę',
				this.onSubmit,
				this
			)
		},
		onSubmit: function (btn, txt) {
			if (btn !== 'ok') {
				return;
			}
			data = {'nazwa': txt};
			console.log(this.combo.store.baseParams);
			Ext.apply(data, this.combo.store.baseParams);
			Ext.Ajax.request({
					method: 'POST',
					jsonData: data,
					url: this.combo.url,
					success: this.onSuccess,
					scope: this
				})
		},
		onSuccess: function () {
			this.combo.store.load();
		},
		setBaseParam: function () {
			console.log('SBP');
			this.combo.setBaseParam.apply(this.combo, arguments);
		}


});

Ext.fi.nz.form = new Ext.form.FormPanel({
		region: 'west',
		width: 500,
		items: [
			Ext.fi.nz.cat_combo = new Ext.fi.nz.CommonCF({
					comboConf: {
						url: 'kategorie',
						fieldLabel: 'Kategoria',
						name: 'kategoria-nazwa',
						hiddenName: 'kategoria-id'
					}
				}),
			Ext.fi.nz.subcat_combo = new Ext.fi.nz.CommonCF({
					comboConf: {
						fieldLabel: 'Podkategoria',
						url: 'podkategorie',
						name: 'podkategoria-nazwa',
						hiddenName: 'podkategoria-id'
					}
				}),
			Ext.fi.nz.product_combo = new Ext.fi.nz.CommonCF({
					comboConf: {
						fieldLabel: 'Produkt',
						url: 'produkty',
						name: 'produkt-nazwa',
						hiddenName: 'produkt-id'
					}
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
		restful: false,
		root: 'zakupy',
		fields: [
			'id', 'produkt-id', 'produkt-nazwa', 'kategoria-id',
			'kategoria-nazwa', 'podkategoria-id', 'podkategoria-nazwa', 'cena',
			'ilosc'],
		writer: new Ext.data.JsonWriter({
				encode: false,
				listful: true
			})
	});

Ext.fi.nz.store.on('write', function (st, action, result) {
		Ext.Msg.alert(
			'Zapisano',
			'Zapisano ' + result.length + ' zakupów',
			window.location.reload,
			window.location
		);
})

Ext.fi.nz.onSubmit = function () {
	Ext.fi.nz.store.setBaseParam('data', Ext.fi.nz.date_field.getValue());
	Ext.fi.nz.store.setBaseParam(
		'sklep', Ext.fi.nz.shop_combo.combo.getValue()
	);
	Ext.fi.nz.store.save();
}

Ext.fi.nz.onDelete = function () {
	Ext.fi.nz.store.remove(Ext.fi.nz.grid.getSelectionModel().getSelected());
}



Ext.fi.nz.grid = new Ext.grid.GridPanel({
		region: 'center',
		store: Ext.fi.nz.store,
		columns: [
			{header: 'Kategoria', dataIndex: 'kategoria-nazwa'},
			{header: 'Podkategoria', dataIndex: 'podkategoria-nazwa'},
			{header: 'Produkt', dataIndex: 'produkt-nazwa'},
			{header: 'Ilość', dataIndex: 'ilosc'},
			{header: 'Cena', dataIndex: 'cena'},
		],
		tbar: [
			new Ext.form.Label({text: 'Sklep:'}),
			Ext.fi.nz.shop_combo = new Ext.fi.nz.CommonCF({
					comboConf: {
						url: 'sklepy',
						width: 200,
						fieldLabel: 'Sklep'
					},
					width: 250
				}),
			new Ext.form.Label({text: 'Data:'}),
			Ext.fi.nz.date_field = new Ext.form.DateField({format: 'Y-m-d'})
		],
		bbar: [
			{
				text: 'Zapisz zakupy',
				handler: Ext.fi.nz.onSubmit
			}, {
				text: 'Usuń zakup',
				handler: Ext.fi.nz.onDelete
			}
		]
	});

Ext.onReady(function () {
		Ext.fi.nz.vp = new Ext.Viewport({
				layout: 'border',
				items: [Ext.fi.nz.form, Ext.fi.nz.grid]
			});
		Ext.fi.nz.cat_combo.combo.on('select', function (combo, rec, i) {
				Ext.fi.nz.subcat_combo.combo.store.setBaseParam(
					'kategoria_id', rec.get('id')
				);
				Ext.fi.nz.subcat_combo.combo.store.load();
			});
		Ext.fi.nz.subcat_combo.combo.on('select', function (combo, rec, i) {
				Ext.fi.nz.product_combo.combo.store.setBaseParam(
					'podkategoria_id', rec.get('id')
				);
				Ext.fi.nz.product_combo.combo.store.load();
			});
	});
