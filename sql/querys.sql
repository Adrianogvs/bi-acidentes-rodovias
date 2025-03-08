SELECT id, concessionaria, "data", horario, n_da_ocorrencia, tipo_de_ocorrencia, km, trecho, sentido, tipo_de_acidente, automovel, bicicleta, caminhao, moto, onibus, outros, tracao_animal, transporte_de_cargas_especiais, trator_maquinas, utilitarios, ilesos, levemente_feridos, moderadamente_feridos, gravemente_feridos, mortos
FROM public.stg_acidentes
;

select *
from dim_rodovia dr ;

select * 
from dim_sentido ds ;

select *
from dim_situacao_acidente dsa ;

select *
from dim_tipo_ocorrencia dto ;

select *
from dim_tipo_veiculo dtv ;

select *
from dim_trecho dt ;

select *
from fato_acidentes fa ;

-- Dimensão Situção do Acidente
with situacao_acidente as (
	SELECT 
	    id, 
	    'ilesos' AS tipo, ilesos AS quantidade FROM public.stg_acidentes
	UNION ALL
	SELECT 
	    id, 
	    'levemente_feridos' AS tipo, levemente_feridos AS quantidade FROM public.stg_acidentes
	UNION ALL
	SELECT 
	    id, 
	    'moderadamente_feridos' AS tipo, moderadamente_feridos AS quantidade FROM public.stg_acidentes
	UNION ALL
	SELECT 
	    id, 
	    'gravemente_feridos' AS tipo, gravemente_feridos AS quantidade FROM public.stg_acidentes
	UNION ALL
	SELECT 
	    id, 
	    'mortos' AS tipo, mortos AS quantidade FROM public.stg_acidentes
),
dim_situacao_acidente as (
	select distinct tipo 
	from situacao_acidente
)
select ROW_NUMBER() OVER (ORDER BY tipo) AS sk, *
from dim_situacao_acidente;

-- Dimensão Veiculo
with dim_veiculo as (
	SELECT 
	    id, 
	    'automovel' AS tipo_veiculo, automovel AS quantidade FROM public.stg_acidentes
	UNION ALL
	SELECT 
	    id, 
	    'bicicleta' AS tipo_veiculo, bicicleta AS quantidade FROM public.stg_acidentes
	UNION ALL
	SELECT 
	    id, 
	    'caminhao' AS tipo_veiculo, caminhao AS quantidade FROM public.stg_acidentes
	UNION ALL
	SELECT 
	    id, 
	    'moto' AS tipo_veiculo, moto AS quantidade FROM public.stg_acidentes
	UNION ALL
	SELECT 
	    id, 
	    'onibus' AS tipo_veiculo, onibus AS quantidade FROM public.stg_acidentes
	UNION ALL
	SELECT 
	    id, 
	    'outros' AS tipo_veiculo, outros AS quantidade FROM public.stg_acidentes
	UNION ALL
	SELECT 
	    id, 
	    'tracao_animal' AS tipo_veiculo, tracao_animal AS quantidade FROM public.stg_acidentes
	UNION ALL
	SELECT 
	    id, 
	    'transporte_de_cargas_especiais' AS tipo_veiculo, transporte_de_cargas_especiais AS quantidade FROM public.stg_acidentes
	UNION ALL
	SELECT 
	    id, 
	    'trator_maquinas' AS tipo_veiculo, trator_maquinas AS quantidade FROM public.stg_acidentes
	UNION ALL
	SELECT 
	    id, 
	    'utilitarios' AS tipo_veiculo, utilitarios AS quantidade FROM public.stg_acidentes

),
dim_tipo_veiculo as (
	select distinct  tipo_veiculo
	from dim_veiculo
)
select  ROW_NUMBER() OVER (ORDER BY tipo_veiculo) AS sk, *
from dim_tipo_veiculo;




-- Dimensão Tipo Ocorrência
with dim_tipo_ocorrencia as (
	select distinct tipo_de_ocorrencia 
	from stg_acidentes sa 
)
select ROW_NUMBER() OVER (ORDER BY tipo_de_ocorrencia) AS sk, *
from dim_tipo_ocorrencia
where tipo_de_ocorrencia is not null;

-- Dimensão Sentido
with dim_sentido as (
	SELECT DISTINCT
	    sentido
	FROM stg_acidentes
)
select ROW_NUMBER() OVER (ORDER BY sentido) AS sk, *
from dim_sentido
where sentido is not null;


-- Dimensão Rodovia
with dim_rodovia as (
	SELECT DISTINCT
	    concessionaria
	FROM stg_acidentes
)
select ROW_NUMBER() OVER (ORDER BY concessionaria) AS sk, *
from dim_rodovia
where concessionaria is not null;


--Dimensão Trecho
with dim_trecho as (
	SELECT DISTINCT
	    trecho
	FROM stg_acidentes
)
select ROW_NUMBER() OVER (ORDER BY trecho) AS sk, *
from dim_trecho
where trecho is not null;


-- total por rodovia
with cte as (
	SELECT concessionaria, COUNT(*) AS total_acidentes
	FROM stg_acidentes
	GROUP BY concessionaria
	ORDER BY total_acidentes desc
)
select sum(total_acidentes) from cte;