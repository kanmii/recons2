# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'IbdInt'
        db.create_table('ibd_int', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('valdate_in_ca', self.gf('django.db.models.fields.DateField')()),
            ('date_processed', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('lc_number', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('overseas_ref', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('ccy', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adhocmodels.Currency'], db_column='ccy')),
            ('bank', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adhocmodels.OverseasBank'], db_column='bank')),
            ('acct', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adhocmodels.NostroAccount'], db_column='acct')),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adhocmodels.Customer'], null=True, db_column='customer', blank=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
            ('valdate_in_pl', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('entry_seq_no', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
        ))
        db.send_create_signal('ibdint', ['IbdInt'])


    def backwards(self, orm):
        # Deleting model 'IbdInt'
        db.delete_table('ibd_int')


    models = {
        'adhocmodels.branch': {
            'Meta': {'ordering': "('name', 'code')", 'object_name': 'Branch', 'db_table': "'branch'"},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'adhocmodels.currency': {
            'Meta': {'ordering': "('code',)", 'object_name': 'Currency', 'db_table': "'currency'"},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'adhocmodels.customer': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Customer', 'db_table': "'customer'"},
            'branch_for_itf': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['adhocmodels.Branch']", 'null': 'True', 'db_column': "'brn_itf'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subsidiaries'", 'null': 'True', 'db_column': "'parent'", 'to': "orm['adhocmodels.Customer']"}),
            'rel_manager': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'clients'", 'null': 'True', 'db_column': "'rel_manager'", 'to': "orm['adhocmodels.RelationshipManager']"})
        },
        'adhocmodels.nostroaccount': {
            'Meta': {'ordering': "('bank',)", 'object_name': 'NostroAccount', 'db_table': "'nostro_acct'"},
            'bank': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'my_nostros'", 'db_column': "'bank'", 'to': "orm['adhocmodels.OverseasBank']"}),
            'ccy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ccy_nostros'", 'db_column': "'ccy'", 'to': "orm['adhocmodels.Currency']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'})
        },
        'adhocmodels.overseasbank': {
            'Meta': {'ordering': "('swift_bic', 'name')", 'object_name': 'OverseasBank', 'db_table': "'overseas_bank'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'swift_bic': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '11'})
        },
        'adhocmodels.relationshipmanager': {
            'Meta': {'ordering': "('name', 'rmcode')", 'object_name': 'RelationshipManager', 'db_table': "'rel_manager'"},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rel_managers'", 'to': "orm['adhocmodels.Branch']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'rmcode': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'})
        },
        'ibdint.ibdint': {
            'Meta': {'ordering': "('date_processed', 'valdate_in_ca')", 'object_name': 'IbdInt', 'db_table': "'ibd_int'"},
            'acct': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['adhocmodels.NostroAccount']", 'db_column': "'acct'"}),
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'bank': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['adhocmodels.OverseasBank']", 'db_column': "'bank'"}),
            'ccy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['adhocmodels.Currency']", 'db_column': "'ccy'"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['adhocmodels.Customer']", 'null': 'True', 'db_column': "'customer'", 'blank': 'True'}),
            'date_processed': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'entry_seq_no': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lc_number': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'overseas_ref': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'valdate_in_ca': ('django.db.models.fields.DateField', [], {}),
            'valdate_in_pl': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['ibdint']