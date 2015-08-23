# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'LCCoverMovement', fields ['lc_number', 'acct', 'date_entry_passed']
        db.create_unique('lc_cv_mvt', ['lc_number', 'acct_id', 'date_entry_passed'])


    def backwards(self, orm):
        # Removing unique constraint on 'LCCoverMovement', fields ['lc_number', 'acct', 'date_entry_passed']
        db.delete_unique('lc_cv_mvt', ['lc_number', 'acct_id', 'date_entry_passed'])


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
        'adhocmodels.ledgeraccount': {
            'Meta': {'object_name': 'LedgerAccount', 'db_table': "'ledger_acct'"},
            'acct_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ledger_acct_types'", 'db_column': "'acct_type'", 'to': "orm['adhocmodels.LedgerAccountType']"}),
            'ccy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['adhocmodels.Currency']", 'db_column': "'ccy'"}),
            'external_number': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lg_numbers'", 'db_column': "'external_number'", 'to_field': "'number'", 'to': u"orm['adhocmodels.NostroAccount']", 'blank': 'True', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default_memo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'})
        },
        'adhocmodels.ledgeraccounttype': {
            'Meta': {'ordering': "('code',)", 'object_name': 'LedgerAccountType', 'db_table': "'ledger_acct_type'"},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'adhocmodels.nostroaccount': {
            'Meta': {'unique_together': "(('bank', 'ccy', 'number'),)", 'object_name': 'NostroAccount', 'db_table': "'nostro_acct'"},
            'bank': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'my_nostros'", 'db_column': "'bank'", 'to': "orm['adhocmodels.OverseasBank']"}),
            'ccy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ccy_nostros'", 'db_column': "'ccy'", 'to': "orm['adhocmodels.Currency']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
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
        'lcavail.lcavailed': {
            'Meta': {'object_name': 'LcAvailed', 'db_table': "'lc_availed'"},
            'avail_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'clarec_detail': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'date_negotiated': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_processed': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dr_cr': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'drawn_amt': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '2'}),
            'entry_seq': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'flex_swift': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lc_number': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'memo_acct': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['adhocmodels.LedgerAccount']", 'db_column': "'memo_acct'"}),
            'nostro_acct': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['adhocmodels.NostroAccount']", 'db_column': "'nostro_acct'"}),
            'unmatched': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'unmatched_lcees'", 'null': 'True', 'to': u"orm['unmatched.UnmatchedRecons']"})
        },
        u'lcavail.lccovermovement': {
            'Meta': {'unique_together': "(('lc_number', 'acct', 'date_entry_passed'),)", 'object_name': 'LCCoverMovement', 'db_table': "'lc_cv_mvt'"},
            'acct': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['adhocmodels.NostroAccount']"}),
            'date_entry_passed': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lc_number': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'swift_text': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        'postentry.entrygeneratingtransaction': {
            'Meta': {'object_name': 'EntryGeneratingTransaction', 'db_table': "'entry_gen_trxn'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        u'unmatched.unmatchedrecons': {
            'Meta': {'object_name': 'UnmatchedRecons', 'db_table': "'unmatched_recons'"},
            'acct_numb': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['adhocmodels.NostroAccount']", 'db_column': "'acct_numb'"}),
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '2'}),
            'clarec_details': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['adhocmodels.Customer']", 'null': 'True', 'blank': 'True'}),
            'date_finally_processed': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_first_uploaded': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_upload_processed': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'entry_seq': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'external_ref': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lc_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'show': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'stmt_or_lg': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'swift': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'trnx_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['postentry.EntryGeneratingTransaction']", 'null': 'True', 'db_column': "'trnx_type'", 'blank': 'True'}),
            'valdate': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['lcavail']