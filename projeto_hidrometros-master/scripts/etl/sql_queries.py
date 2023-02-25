hidrometros_producao_quantidade = 'select count(*) from tmp.aux_hid_medidor'

hidrometros_producao_medicoes = '''
SELECT DISTINCT
	MED.MED_NUM_MEDIDOR, 
	MED.MED_NUM_SEQ_MEDIDOR,
	MED.MED_DAT_CADASTRO_MEDIDOR,
	MED.MAR_SEQ_MARCA,
	MED.ILM_SEQ_ITEM_LOTE_MEDIDOR,
	MED.MED_STA_MEDIDOR,
	MED.ESM_SEQ_ESPECIFICACAO_MEDIDOR,
	INS.INS_DAT_INSTALACAO_MEDIDOR,
	INS.INS_DAT_RETIRADA_MEDIDOR,
	MDC.MED_NUM_LEITURA_CAMPO_ANT,
	MDC.MED_NUM_LEITURA_PROC_ANT,
	MDC.MED_NUM_LEITURA_CAMPO_ATUAL,
	MDC.MED_NUM_LEITURA_PROC_ATUAL,
	MDC.MED_DAT_LEITURA,
	MDC.OCL_SEQ_OCORRENCIA_CAMPO,
	INS.IMO_COD_INSCRICAO,
	INS.PRO_SEQ_PRODUTO,
	INS. qtd_instalacao,
	MED.MED_SEQ_MEDIDOR,
	IMO.*
FROM tmp.aux_hid_medicoes MDC
JOIN tmp.aux_hid_instalacoes  INS 	ON INS.INS_SEQ_INSTALACAO=MDC.INS_SEQ_INSTALACAO
JOIN tmp.aux_hid_medidor MED 		ON MED.MED_SEQ_MEDIDOR = INS.MED_SEQ_MEDIDOR 
join tmp.aux_hid_imovel IMO ON ins.IMO_COD_INSCRICAO=imo.hid_imo_cod_inscricao
where MED.MED_SEQ_MEDIDOR IN (
select distinct 
		MED.MED_SEQ_MEDIDOR
FROM tmp.aux_hid_medicoes MDC
JOIN tmp.aux_hid_instalacoes  INS 	ON INS.INS_SEQ_INSTALACAO=MDC.INS_SEQ_INSTALACAO
JOIN tmp.aux_hid_medidor MED 		ON MED.MED_SEQ_MEDIDOR = INS.MED_SEQ_MEDIDOR 
where ins.INS_DAT_RETIRADA_MEDIDOR is null 
ORDER BY MED.MED_SEQ_MEDIDOR
limit 40000 offset {}
)
AND ins.INS_DAT_RETIRADA_MEDIDOR is null 
and hid_imo_cod_tip_registro='PROD'
ORDER BY MED.MED_SEQ_MEDIDOR, MDC.MED_DAT_LEITURA
'''

hidrometros_bancada_medicoes = '''
select 
  hmh_num_medidor MED_NUM_MEDIDOR, 
  hmh_num_seq_medidor  MED_NUM_SEQ_MEDIDOR,
  hmh_dat_cadastro_medidor MED_DAT_CADASTRO_MEDIDOR,
  hmh_cod_marca MAR_SEQ_MARCA,
  hmh_cod_item_lote_medidor ILM_SEQ_ITEM_LOTE_MEDIDOR,
  hmh_cod_sta_medidor MED_STA_MEDIDOR,
  hmh_cod_especificacao_medidor ESM_SEQ_ESPECIFICACAO_MEDIDOR,
  hmh_dat_instalacao_medidor INS_DAT_INSTALACAO_MEDIDOR,
  hmh_dat_retirada_medidor INS_DAT_RETIRADA_MEDIDOR,
  hmh_num_leitura_campo_ant MED_NUM_LEITURA_CAMPO_ANT,
  hmh_num_leitura_proc_ant MED_NUM_LEITURA_PROC_ANT,
  hmh_num_leitura_campo_atual MED_NUM_LEITURA_CAMPO_ATUAL,
  hmh_num_leitura_proc_atual MED_NUM_LEITURA_PROC_ATUAL,
  hmh_dat_leitura MED_DAT_LEITURA,
  hmh_cod_ocorrencia_campo OCL_SEQ_OCORRENCIA_CAMPO,
  hmh_cod_inscricao IMO_COD_INSCRICAO,
  hmh_cod_produto PRO_SEQ_PRODUTO,
  hmh_dat_qtd_instalacao qtd_instalacao,
  hmh_num_medidor||hmh_num_seq_medidor  MED_SEQ_MEDIDOR,
  imo.*
from ml.hid_hmh_historico_medicao_hidrometro hmh
join ml.hid_imo_imovel  imo on hmh.hmh_cod_inscricao=imo.hid_imo_cod_inscricao 
order by  hmh_num_medidor||hmh_num_seq_medidor , hmh_dat_leitura
'''

analise_bancada_completa = '''
select * from ml.hid_bhc_bancada_hidrometro_cliente
'''

imoveis_ativos = '''
select distinct 
	padrao_imovel.pim_dsc_padrao_imovel,
	sit_imo.sii_nom_situacao_imovel,
	lig_agua.sla_nom_situacao_lig_agua,
	imo.imo_bsk_imovel,
	geo.geo_set_num_setor,
	geo.geo_lge_dsc_municipio_prax,
	geo.geo_lge_dsc_distrito_prax,
	geo.geo_lge_dsc_localidade_prax,
	geo.geo_uad_sgl_unidade_negocio
from dw.fat_imo_imovel fato
join dw.dim_imo_imovel imo 
	on fato.imo_srk_imovel=imo.imo_srk_imovel
join dw.dim_geo_geografia_corporativa geo
	on fato.geo_srk_geografia=geo.geo_srk_geografia
join dw.dim_sii_situacao_imovel sit_imo 
	on fato.sii_srk_situacao_imovel = sit_imo.sii_srk_situacao_imovel
join dw.dim_sla_situacao_lig_agua lig_agua 
	on fato.sla_srk_situacao_lig_agua = lig_agua.sla_srk_situacao_lig_agua
join dw.dim_pim_padrao_imovel padrao_imovel 
	on fato.pim_srk_padrao_imovel = padrao_imovel.pim_srk_padrao_imovel
join dw.dim_tem_tempo tempo 
	on fato.tem_srk_tempo=tempo.tem_srk_tempo
where imo.imo_dat_fim_vigencia is null
	and tempo.tem_des_ano_mes = {}
'''

IMOVEIS_ATIVOS_PRODUCAO = """
select 
	imo.imo_cod_inscricao imo_bsk_imovel,  
	setr.set_num_setor geo_set_num_setor, 
	loc.lge_nom_local_geografico geo_lge_dsc_localidade_prax,
	dis.lge_nom_local_geografico geo_lge_dsc_distrito_prax,
	mun.lge_nom_local_geografico geo_lge_dsc_municipio_prax,
	uad.uad_sgl_unidade_administrativa geo_uad_sgl_unidade_negocio,
	pim.pim_nom_padrao_imovel pim_dsc_padrao_imovel,
	sii.sii_nom_situacao_imovel sii_nom_situacao_imovel,
	lig.lig_cod_est_ligacao  sla_nom_situacao_lig_agua	
from imo_imovel imo 
left outer join lig_ligacao lig 
	on imo.imo_cod_inscricao = lig.imo_cod_inscricao and lig.lig_tip_ligacao = 'A',
	pim_padrao_imovel pim, 
	sii_situacao_imovel sii, 
	lot_lote lot, 
	qua_quadra qua, 
	set_setor setr,
	uad_unidade_administrativa uad,
	lge_local_geografico loc, 
	lge_local_geografico dis, 
	lge_local_geografico mun
where imo.pim_seq_padrao_imovel = pim.pim_seq_padrao_imovel
	and imo.sii_seq_situacao_imovel = sii.sii_seq_situacao_imovel
	and imo.lot_seq_lote = lot.lot_seq_lote
	and lot.qua_seq_quadra = qua.qua_seq_quadra
	and qua.set_seq_setor = setr.set_seq_setor
	and setr.uad_cod_unidade_administrativa = uad.uad_cod_unidade_administrativa
	and setr.lge_seq_local_geografico = loc.lge_seq_local_geografico
	and loc.lge_cod_distrito = dis.lge_seq_local_geografico
	and loc.lge_cod_municipio = mun.lge_seq_local_geografico
	and lig.lig_cod_est_ligacao = 1
	AND NOT EXISTS (
			SELECT *
		FROM ITA_ITEM_ATENDIMENTO 
		WHERE  STA_SEQ_STATUS_ATENDIMENTO=5
			AND ISS_DAT_EXECUCAO_INFORMADA IS NULL
			AND ISS_DAT_CANCELAMENTO IS null
			AND SER_SEQ_SERVICO IN (
			  	SELECT SER_SEQ_SERVICO_FILHO
				FROM srs_servico_restringe_ss
				WHERE ser_seq_servico_pai = 44349
				AND IMO_COD_INSCRICAO = imo.imo_cod_inscricao
	 )
	)
"""

predicoes_realizadas = '''
select DISTINCT
	hid.IDHidrometro,
	imo.hid_imo_cod_inscricao,
	hid.CVProcessado,
	hid.QtdMedicoes,
	hid.QtdOcorrencias,
	hid.hid_imo_qtd_pontos_utilizacao,
	hid.variacaoTendencia,
	hid.vidaHidrometro,
	hid.vidaInstalacao,
	hid.predicao,
	hid.proba_0,
	est.ESM_SEQ_ESPECIFICACAO_MEDIDOR,
	est.MED_NUM_VOLUME_CALCULADO,
	est.MED_NUM_VOLUME_MEDIDO
from tmp.aux_hid_medicoes mdc 
join tmp.aux_hid_instalacoes ins 
	on mdc.INS_SEQ_INSTALACAO=ins.INS_SEQ_INSTALACAO
join tmp.aux_hid_medidor med 
	on ins.MED_SEQ_MEDIDOR=med.MED_SEQ_MEDIDOR
join tmp.aux_hid_imovel imo 
	on imo.hid_imo_cod_inscricao=ins.IMO_COD_INSCRICAO
join tmp.aux_hid_medicoes_estatistica est 
	on med.MED_SEQ_MEDIDOR = est.MED_SEQ_MEDIDOR 
join tmp.hid_prd_predicoes_modelo hid 
		on med.MED_NUM_MEDIDOR||med.MED_NUM_SEQ_MEDIDOR = hid.IDHidrometro
where hid_imo_cod_tip_registro='PROD'
'''