-- create table pessoa
-- depends: 
CREATE TABLE public.pessoas (
  id              VARCHAR PRIMARY KEY,
  nome            VARCHAR,
  cpf             VARCHAR,
  rg              VARCHAR,
  data_nascimento DATE,
  telefones       JSONB
);
