-- =====================================================================
--  MINHA ENGINE - servidor online (Supabase)
--  Cole TUDO isto no Supabase: SQL Editor > New query > Run.
--  Pode rodar de novo quando eu mandar uma versao nova (ele so atualiza).
-- =====================================================================

-- ---------------------------------------------------------------------
-- TABELAS
-- ---------------------------------------------------------------------
create table if not exists public.planos (
  nome text primary key,
  preco int not null,
  bonus int not null,           -- Brasas por semana
  vender int not null,          -- quantos itens pode ter a venda na Loja
  desconto int not null,        -- % de desconto na Loja
  taxa int not null,            -- % que a Loja fica das vendas
  ordem int not null
);
insert into public.planos (nome, preco, bonus, vender, desconto, taxa, ordem) values
  ('Grátis', 0, 10, 1, 0, 30, 0),
  ('Game Maker', 300, 35, 10, 10, 15, 1),
  ('Dev', 800, 75, 999, 25, 5, 2)
on conflict (nome) do update set preco = excluded.preco, bonus = excluded.bonus, vender = excluded.vender,
  desconto = excluded.desconto, taxa = excluded.taxa, ordem = excluded.ordem;

create table if not exists public.perfis (
  id uuid primary key,
  nome text not null unique check (char_length(nome) between 2 and 24),
  saldo bigint not null default 0 check (saldo >= 0),
  plano text not null default 'Grátis' references public.planos (nome),
  plano_ate timestamptz,
  ultima_recompensa text not null default '',
  criado timestamptz not null default now()
);
create unique index if not exists perfis_nome_minusculo on public.perfis (lower(nome));

create table if not exists public.historico (
  id bigserial primary key,
  usuario uuid not null references public.perfis (id) on delete cascade,
  valor bigint not null,
  motivo text not null,
  quando timestamptz not null default now()
);
create index if not exists historico_usuario on public.historico (usuario, quando desc);

create table if not exists public.conquistas (
  usuario uuid not null references public.perfis (id) on delete cascade,
  chave text not null,
  quando timestamptz not null default now(),
  primary key (usuario, chave)
);

create table if not exists public.compras (
  usuario uuid not null references public.perfis (id) on delete cascade,
  item text not null,
  preco int not null default 0,
  quando timestamptz not null default now(),
  primary key (usuario, item)
);

create table if not exists public.jogos (
  id uuid primary key default gen_random_uuid(),
  autor uuid not null default auth.uid() references public.perfis (id) on delete cascade,
  titulo text not null check (char_length(titulo) between 1 and 40),
  descricao text not null default '' check (char_length(descricao) <= 200),
  arquivo text not null,
  miniatura text not null default '',
  visitas int not null default 0,
  likes int not null default 0,
  denuncias int not null default 0,
  oculto boolean not null default false,
  publicado timestamptz not null default now(),
  atualizado timestamptz not null default now()
);
create index if not exists jogos_autor on public.jogos (autor);

create table if not exists public.visitas (
  jogo uuid not null references public.jogos (id) on delete cascade,
  usuario uuid not null references public.perfis (id) on delete cascade,
  quando timestamptz not null default now(),
  primary key (jogo, usuario)
);
create table if not exists public.likes (
  jogo uuid not null references public.jogos (id) on delete cascade,
  usuario uuid not null references public.perfis (id) on delete cascade,
  quando timestamptz not null default now(),
  primary key (jogo, usuario)
);
create table if not exists public.denuncias (
  jogo uuid not null references public.jogos (id) on delete cascade,
  usuario uuid not null references public.perfis (id) on delete cascade,
  motivo text not null default '',
  quando timestamptz not null default now(),
  primary key (jogo, usuario)
);

create table if not exists public.itens_venda (
  id uuid primary key default gen_random_uuid(),
  autor uuid not null default auth.uid() references public.perfis (id) on delete cascade,
  nome text not null check (char_length(nome) between 1 and 40),
  descricao text not null default '' check (char_length(descricao) <= 160),
  categoria text not null default 'Outros',
  preco int not null default 0 check (preco between 0 and 9999),
  pacote jsonb not null check (octet_length(pacote::text) < 3000000),
  vendas int not null default 0,
  criado timestamptz not null default now()
);
create index if not exists itens_venda_autor on public.itens_venda (autor);

-- ---------------------------------------------------------------------
-- FUNCOES (tudo que mexe com Brasas roda AQUI no servidor, ninguem trapaceia)
-- ---------------------------------------------------------------------
create or replace function public.plano_de(u uuid) returns text
language sql stable security definer set search_path = public as $$
  select coalesce((select case when p.plano <> 'Grátis' and p.plano_ate > now() then p.plano else 'Grátis' end
                   from public.perfis p where p.id = u), 'Grátis')
$$;

create or replace function public._mover(u uuid, v bigint, motivo text) returns bigint
language plpgsql security definer set search_path = public as $$
declare s bigint;
begin
  update public.perfis set saldo = greatest(0, saldo + v) where id = u returning saldo into s;
  insert into public.historico (usuario, valor, motivo) values (u, v, left(motivo, 60));
  return s;
end $$;
revoke execute on function public._mover(uuid, bigint, text) from public, anon, authenticated;

-- cria o perfil da pessoa (a engine chama isso logo depois de criar a conta)
create or replace function public.garantir_perfil(p_nome text default '') returns boolean
language plpgsql security definer set search_path = public as $$
declare base text; tentativa text; email text; criou int;
begin
  if auth.uid() is null then return false; end if;
  if exists (select 1 from public.perfis where id = auth.uid()) then return true; end if;
  email := coalesce(auth.jwt() ->> 'email', 'criador');
  base := left(regexp_replace(coalesce(nullif(trim(p_nome), ''), nullif(trim(auth.jwt() -> 'user_metadata' ->> 'nome'), ''),
                                       split_part(email, '@', 1)), '\s+', ' ', 'g'), 19);
  if char_length(base) < 2 then base := base || 'Criador'; end if;
  tentativa := base;
  while exists (select 1 from public.perfis where lower(nome) = lower(tentativa)) loop
    tentativa := base || (floor(random() * 9000) + 1000)::int;
  end loop;
  -- duas chamadas ao mesmo tempo (login + carteira) nao podem dar erro: a segunda so nao faz nada
  insert into public.perfis (id, nome, saldo) values (auth.uid(), tentativa, 150) on conflict (id) do nothing;
  get diagnostics criou = row_count;
  if criou = 0 then return true; end if;
  insert into public.historico (usuario, valor, motivo) values (auth.uid(), 150, 'Presente de boas-vindas');
  insert into public.conquistas (usuario, chave) values (auth.uid(), 'boas_vindas') on conflict do nothing;
  return true;
end $$;

-- o nome ainda esta livre? (para a tela de criar conta)
create or replace function public.nome_livre(p_nome text) returns boolean
language sql stable security definer set search_path = public as $$
  select not exists (select 1 from public.perfis where lower(nome) = lower(trim(p_nome)))
$$;

create or replace function public.renomear(p_nome text) returns json
language plpgsql security definer set search_path = public as $$
declare n text := trim(regexp_replace(coalesce(p_nome, ''), '\s+', ' ', 'g'));
begin
  if auth.uid() is null then return json_build_object('ok', false, 'msg', 'Entre na sua conta primeiro.'); end if;
  if char_length(n) < 2 or char_length(n) > 24 then
    return json_build_object('ok', false, 'msg', 'O nome precisa ter de 2 a 24 letras.'); end if;
  if exists (select 1 from public.perfis where lower(nome) = lower(n) and id <> auth.uid()) then
    return json_build_object('ok', false, 'msg', 'Esse nome já é de outra pessoa.'); end if;
  update public.perfis set nome = n where id = auth.uid();
  return json_build_object('ok', true, 'msg', 'Nome trocado para ' || n || '.');
end $$;

-- tudo da carteira de uma vez
create or replace function public.minha_carteira() returns json
language sql stable security definer set search_path = public as $$
  select json_build_object(
    'id', p.id, 'nome', p.nome, 'saldo', p.saldo, 'plano', public.plano_de(p.id),
    'plano_ate', extract(epoch from p.plano_ate), 'ultima_recompensa', p.ultima_recompensa,
    'semana', to_char(now(), 'IYYY-"S"IW'),
    'comprados', coalesce((select json_agg(c.item) from public.compras c where c.usuario = p.id), '[]'),
    'conquistas', coalesce((select json_agg(q.chave) from public.conquistas q where q.usuario = p.id), '[]'),
    'historico', coalesce((select json_agg(json_build_object('valor', h.valor, 'motivo', h.motivo,
                                   'data', to_char(h.quando at time zone 'America/Sao_Paulo', 'DD/MM HH24:MI'))
                                   order by h.quando)
                           from (select * from public.historico where usuario = p.id order by quando desc limit 40) h),
                          '[]'),
    'vendas', coalesce((select sum(i.vendas) from public.itens_venda i where i.autor = p.id), 0))
  from public.perfis p where p.id = auth.uid()
$$;

-- recompensa da semana (1 vez por semana)
create or replace function public.pegar_recompensa() returns int
language plpgsql security definer set search_path = public as $$
declare semana text := to_char(now(), 'IYYY-"S"IW'); v int;
begin
  if auth.uid() is null then return 0; end if;
  update public.perfis set ultima_recompensa = semana where id = auth.uid() and ultima_recompensa <> semana;
  if not found then return 0; end if;
  select bonus into v from public.planos where nome = public.plano_de(auth.uid());
  perform public._mover(auth.uid(), v, 'Recompensa semanal (' || public.plano_de(auth.uid()) || ')');
  return v;
end $$;

-- assinar ou renovar um plano (1 mes)
create or replace function public.assinar(p_plano text) returns json
language plpgsql security definer set search_path = public as $$
declare pl public.planos; atual text; at_ordem int; p public.perfis; base timestamptz;
begin
  if auth.uid() is null then return json_build_object('ok', false, 'msg', 'Entre na sua conta primeiro.'); end if;
  select * into pl from public.planos where nome = p_plano;
  if pl is null or pl.preco = 0 then return json_build_object('ok', false, 'msg', 'Esse plano não existe.'); end if;
  select * into p from public.perfis where id = auth.uid() for update;
  atual := public.plano_de(auth.uid());
  select ordem into at_ordem from public.planos where nome = atual;
  if pl.ordem < at_ordem then
    return json_build_object('ok', false, 'msg', 'Você já tem o plano ' || atual || ', que é melhor. Espere ele acabar.');
  end if;
  if p.saldo < pl.preco then
    return json_build_object('ok', false, 'msg', 'Faltam ' || (pl.preco - p.saldo) || ' Brasas para o plano ' || pl.nome
                             || '. Publique jogos: visita +25, like +50!');
  end if;
  base := case when atual = pl.nome and p.plano_ate > now() then p.plano_ate else now() end;
  update public.perfis set plano = pl.nome, plano_ate = base + interval '1 month' where id = auth.uid();
  perform public._mover(auth.uid(), -pl.preco, 'Plano ' || pl.nome || ' (1 mês)');
  return json_build_object('ok', true, 'msg', 'Pronto! Agora você é ' || pl.nome || ' por 1 mês.');
end $$;

-- comprar item pronto da Loja (o desconto do plano e aplicado aqui)
create or replace function public.comprar_da_loja(p_item text, p_preco int) returns json
language plpgsql security definer set search_path = public as $$
declare d int; v int; s bigint;
begin
  if auth.uid() is null then return json_build_object('ok', false, 'msg', 'Entre na sua conta primeiro.'); end if;
  if p_item not like 'loja:%' or p_preco < 0 or p_preco > 1000 then
    return json_build_object('ok', false, 'msg', 'Item inválido.'); end if;
  if exists (select 1 from public.compras where usuario = auth.uid() and item = p_item) then
    return json_build_object('ok', true, 'msg', 'Você já tem esse item.'); end if;
  select desconto into d from public.planos where nome = public.plano_de(auth.uid());
  v := round(p_preco * (100 - d) / 100.0);
  select saldo into s from public.perfis where id = auth.uid() for update;
  if s < v then return json_build_object('ok', false, 'msg', 'Faltam ' || (v - s) || ' Brasas.'); end if;
  insert into public.compras (usuario, item, preco) values (auth.uid(), p_item, v);
  perform public._mover(auth.uid(), -v, 'Comprou ''' || substr(p_item, 6) || '''');
  return json_build_object('ok', true, 'msg', 'Comprou por ' || v || ' Brasas!');
end $$;

-- comprar item que outra pessoa esta vendendo (as Brasas vao para ela, menos a taxa)
create or replace function public.comprar_item(p_item uuid) returns json
language plpgsql security definer set search_path = public as $$
declare it public.itens_venda; d int; t int; v int; ganho int; s bigint; nome_comprador text;
begin
  if auth.uid() is null then return json_build_object('ok', false, 'msg', 'Entre na sua conta primeiro.'); end if;
  select * into it from public.itens_venda where id = p_item;
  if it is null then return json_build_object('ok', false, 'msg', 'Esse item não está mais à venda.'); end if;
  if it.autor = auth.uid() then return json_build_object('ok', true, 'msg', 'Esse item é seu.'); end if;
  if exists (select 1 from public.compras where usuario = auth.uid() and item = p_item::text) then
    return json_build_object('ok', true, 'msg', 'Você já tem esse item.'); end if;
  select desconto into d from public.planos where nome = public.plano_de(auth.uid());
  select taxa into t from public.planos where nome = public.plano_de(it.autor);
  v := round(it.preco * (100 - d) / 100.0);
  select saldo into s from public.perfis where id = auth.uid() for update;
  if s < v then return json_build_object('ok', false, 'msg', 'Faltam ' || (v - s) || ' Brasas.'); end if;
  select nome into nome_comprador from public.perfis where id = auth.uid();
  insert into public.compras (usuario, item, preco) values (auth.uid(), p_item::text, v);
  update public.itens_venda set vendas = vendas + 1 where id = p_item;
  if v > 0 then
    perform public._mover(auth.uid(), -v, 'Comprou ''' || it.nome || '''');
    ganho := it.preco - (it.preco * t / 100);
    perform public._mover(it.autor, ganho, 'Venda de ''' || it.nome || ''' para ' || nome_comprador);
  end if;
  return json_build_object('ok', true, 'msg', case when v > 0 then 'Comprou por ' || v || ' Brasas!' else 'Pegou de graça!' end);
end $$;

-- conquistas (cada uma vale 1 vez)
create or replace function public.conquista(p_chave text) returns int
language plpgsql security definer set search_path = public as $$
declare v int; motivo text;
begin
  if auth.uid() is null then return 0; end if;
  select x.v, x.m into v, motivo from (values ('primeiros_passos', 50, 'Completou os Primeiros passos'),
    ('primeira_exportacao', 30, 'Exportou o primeiro jogo'), ('primeiro_item_a_venda', 20, 'Colocou o primeiro item à venda'),
    ('primeiro_jogo_publicado', 20, 'Publicou o primeiro jogo')) as x(k, v, m) where x.k = p_chave;
  if v is null then return 0; end if;
  insert into public.conquistas (usuario, chave) values (auth.uid(), p_chave) on conflict do nothing;
  if not found then return 0; end if;
  perform public._mover(auth.uid(), v, motivo);
  return v;
end $$;

-- alguem jogou: +25 para o autor (1 vez por pessoa)
create or replace function public.registrar_visita(p_jogo uuid) returns int
language plpgsql security definer set search_path = public as $$
declare a uuid; titulo_ text; quem text;
begin
  if auth.uid() is null then return 0; end if;
  select autor, titulo into a, titulo_ from public.jogos where id = p_jogo;
  if a is null or a = auth.uid() then return 0; end if;
  insert into public.visitas (jogo, usuario) values (p_jogo, auth.uid()) on conflict do nothing;
  if not found then return 0; end if;
  update public.jogos set visitas = visitas + 1 where id = p_jogo;
  select nome into quem from public.perfis where id = auth.uid();
  perform public._mover(a, 25, 'Visita de ' || quem || ' em ''' || titulo_ || '''');
  return 25;
end $$;

-- like: +50 para o autor (1 vez por pessoa)
create or replace function public.curtir(p_jogo uuid) returns json
language plpgsql security definer set search_path = public as $$
declare a uuid; titulo_ text; quem text;
begin
  if auth.uid() is null then return json_build_object('ok', false, 'msg', 'Entre na sua conta para curtir.'); end if;
  select autor, titulo into a, titulo_ from public.jogos where id = p_jogo;
  if a is null then return json_build_object('ok', false, 'msg', 'Esse jogo não existe mais.'); end if;
  if a = auth.uid() then return json_build_object('ok', false, 'msg', 'Você não pode curtir o seu próprio jogo.'); end if;
  insert into public.likes (jogo, usuario) values (p_jogo, auth.uid()) on conflict do nothing;
  if not found then return json_build_object('ok', false, 'msg', 'Você já curtiu esse jogo.'); end if;
  update public.jogos set likes = likes + 1 where id = p_jogo;
  select nome into quem from public.perfis where id = auth.uid();
  perform public._mover(a, 50, 'Like de ' || quem || ' em ''' || titulo_ || '''');
  return json_build_object('ok', true, 'msg', 'Curtiu ''' || titulo_ || '''! O autor ganhou 50 Brasas.');
end $$;

-- denunciar jogo improprio (com 5 denuncias ele some da lista)
create or replace function public.denunciar(p_jogo uuid, p_motivo text) returns text
language plpgsql security definer set search_path = public as $$
begin
  if auth.uid() is null then return 'Entre na sua conta para denunciar.'; end if;
  if exists (select 1 from public.jogos where id = p_jogo and autor = auth.uid()) then
    return 'Esse jogo é seu.'; end if;
  insert into public.denuncias (jogo, usuario, motivo) values (p_jogo, auth.uid(), left(coalesce(p_motivo, ''), 200))
    on conflict do nothing;
  if not found then return 'Você já denunciou esse jogo.'; end if;
  update public.jogos set denuncias = denuncias + 1, oculto = (denuncias + 1 >= 5) where id = p_jogo;
  return 'Denúncia enviada. Obrigado por ajudar!';
end $$;

-- codigo secreto (a senha fica guardada embaralhada)
create or replace function public.codigo_secreto(p_senha text) returns json
language plpgsql security definer set search_path = public as $$
begin
  if auth.uid() is null then return json_build_object('ok', false, 'msg', 'Entre na sua conta primeiro.'); end if;
  if encode(extensions.digest('minha-engine:' || coalesce(p_senha, ''), 'sha256'), 'hex')
     <> 'f679180cc524c5e78522a1bbafac46b1f51ea464e2815d9364b3517a67dae1ef' then
    return json_build_object('ok', false, 'msg', 'Senha errada.');
  end if;
  perform public._mover(auth.uid(), 99999999, 'Código secreto');
  return json_build_object('ok', true, 'msg', 'Código secreto! +99.999.999 Brasas');
end $$;

revoke execute on function public.pegar_recompensa(), public.assinar(text), public.comprar_da_loja(text, int),
  public.comprar_item(uuid), public.conquista(text), public.registrar_visita(uuid), public.curtir(uuid),
  public.denunciar(uuid, text), public.codigo_secreto(text), public.minha_carteira(), public.renomear(text),
  public.garantir_perfil(text)
  from public, anon;
grant execute on function public.pegar_recompensa(), public.assinar(text), public.comprar_da_loja(text, int),
  public.comprar_item(uuid), public.conquista(text), public.registrar_visita(uuid), public.curtir(uuid),
  public.denunciar(uuid, text), public.codigo_secreto(text), public.minha_carteira(), public.renomear(text),
  public.garantir_perfil(text)
  to authenticated;
grant execute on function public.nome_livre(text) to anon, authenticated;
revoke execute on function public.plano_de(uuid) from public, anon;
grant execute on function public.plano_de(uuid) to authenticated;

-- ---------------------------------------------------------------------
-- QUEM PODE VER E MUDAR O QUE (Row Level Security)
-- O dinheiro (saldo), likes, visitas e vendas SO mudam pelas funcoes la de baixo.
-- ---------------------------------------------------------------------
alter table public.planos enable row level security;
alter table public.perfis enable row level security;
alter table public.historico enable row level security;
alter table public.conquistas enable row level security;
alter table public.compras enable row level security;
alter table public.jogos enable row level security;
alter table public.visitas enable row level security;
alter table public.likes enable row level security;
alter table public.denuncias enable row level security;
alter table public.itens_venda enable row level security;

revoke insert, update, delete, truncate on public.planos, public.perfis, public.historico, public.conquistas,
  public.compras, public.jogos, public.visitas, public.likes, public.denuncias, public.itens_venda from anon, authenticated;
grant select on public.planos, public.perfis, public.historico, public.conquistas, public.compras, public.jogos,
  public.visitas, public.likes, public.itens_venda to anon, authenticated;
revoke select on public.denuncias from anon, authenticated;
-- so estas colunas o dono pode escrever direto
grant insert (titulo, descricao, arquivo, miniatura) on public.jogos to authenticated;
grant update (titulo, descricao, arquivo, miniatura, atualizado) on public.jogos to authenticated;
grant delete on public.jogos to authenticated;
grant insert (nome, descricao, categoria, preco, pacote) on public.itens_venda to authenticated;
grant update (nome, descricao, categoria, preco) on public.itens_venda to authenticated;
grant delete on public.itens_venda to authenticated;

drop policy if exists "planos: todos veem" on public.planos;
create policy "planos: todos veem" on public.planos for select using (true);

drop policy if exists "perfis: todos veem" on public.perfis;
create policy "perfis: todos veem" on public.perfis for select using (true);

drop policy if exists "historico: so o seu" on public.historico;
create policy "historico: so o seu" on public.historico for select using (usuario = auth.uid());
drop policy if exists "conquistas: so as suas" on public.conquistas;
create policy "conquistas: so as suas" on public.conquistas for select using (usuario = auth.uid());
drop policy if exists "compras: so as suas" on public.compras;
create policy "compras: so as suas" on public.compras for select using (usuario = auth.uid());
drop policy if exists "visitas: so as suas" on public.visitas;
create policy "visitas: so as suas" on public.visitas for select using (usuario = auth.uid());
drop policy if exists "likes: so os seus" on public.likes;
create policy "likes: so os seus" on public.likes for select using (usuario = auth.uid());

drop policy if exists "jogos: todos veem" on public.jogos;
create policy "jogos: todos veem" on public.jogos for select using (not oculto or autor = auth.uid());
drop policy if exists "jogos: publicar" on public.jogos;
create policy "jogos: publicar" on public.jogos for insert to authenticated
  with check (autor = auth.uid() and (select count(*) from public.jogos j where j.autor = auth.uid()) < 50);
drop policy if exists "jogos: atualizar os seus" on public.jogos;
create policy "jogos: atualizar os seus" on public.jogos for update to authenticated
  using (autor = auth.uid()) with check (autor = auth.uid());
drop policy if exists "jogos: apagar os seus" on public.jogos;
create policy "jogos: apagar os seus" on public.jogos for delete to authenticated using (autor = auth.uid());

drop policy if exists "itens: todos veem" on public.itens_venda;
create policy "itens: todos veem" on public.itens_venda for select using (true);
drop policy if exists "itens: vender" on public.itens_venda;
create policy "itens: vender" on public.itens_venda for insert to authenticated
  with check (autor = auth.uid() and (select count(*) from public.itens_venda i where i.autor = auth.uid())
              < (select p.vender from public.planos p where p.nome = public.plano_de(auth.uid())));
drop policy if exists "itens: mudar os seus" on public.itens_venda;
create policy "itens: mudar os seus" on public.itens_venda for update to authenticated
  using (autor = auth.uid()) with check (autor = auth.uid());
drop policy if exists "itens: tirar os seus" on public.itens_venda;
create policy "itens: tirar os seus" on public.itens_venda for delete to authenticated using (autor = auth.uid());

-- ---------------------------------------------------------------------
-- ARQUIVOS DOS JOGOS (Storage): cada pessoa so mexe na pasta dela
-- ---------------------------------------------------------------------
do $storage$
begin
  insert into storage.buckets (id, name, public, file_size_limit)
  values ('jogos', 'jogos', true, 52428800)
  on conflict (id) do update set public = true, file_size_limit = 52428800;
  execute 'drop policy if exists "jogos: ver arquivos" on storage.objects';
  execute 'create policy "jogos: ver arquivos" on storage.objects for select using (bucket_id = ''jogos'')';
  execute 'drop policy if exists "jogos: enviar na sua pasta" on storage.objects';
  execute 'create policy "jogos: enviar na sua pasta" on storage.objects for insert to authenticated
    with check (bucket_id = ''jogos'' and (storage.foldername(name))[1] = auth.uid()::text)';
  execute 'drop policy if exists "jogos: trocar na sua pasta" on storage.objects';
  execute 'create policy "jogos: trocar na sua pasta" on storage.objects for update to authenticated
    using (bucket_id = ''jogos'' and (storage.foldername(name))[1] = auth.uid()::text)
    with check (bucket_id = ''jogos'' and (storage.foldername(name))[1] = auth.uid()::text)';
  execute 'drop policy if exists "jogos: apagar da sua pasta" on storage.objects';
  execute 'create policy "jogos: apagar da sua pasta" on storage.objects for delete to authenticated
    using (bucket_id = ''jogos'' and (storage.foldername(name))[1] = auth.uid()::text)';
exception when others then
  raise warning 'Storage nao configurado: %', sqlerrm;
end
$storage$;

-- ---------------------------------------------------------------------
-- CODIGOS PROMOCIONAIS (so o hash fica salvo: ninguem le os codigos)
-- ---------------------------------------------------------------------
create table if not exists public.codigos (
  hash text primary key, brasas int not null default 0, plano text references public.planos (nome),
  dias int not null default 0, ativo boolean not null default true, limite int, usos int not null default 0,
  criado timestamptz not null default now());
alter table public.codigos enable row level security;
revoke all on public.codigos from anon, authenticated;
create table if not exists public.codigos_usados (
  usuario uuid not null references public.perfis (id) on delete cascade,
  hash text not null references public.codigos (hash) on delete cascade,
  quando timestamptz not null default now(), primary key (usuario, hash));
alter table public.codigos_usados enable row level security;
revoke all on public.codigos_usados from anon, authenticated;
create or replace function public.usar_codigo(p_codigo text) returns json
language plpgsql security definer set search_path = public as $$
declare c public.codigos; h text; atual text; at_ordem int; cod_ordem int; base timestamptz; p public.perfis; partes text[] := '{}';
begin
  if auth.uid() is null then return json_build_object('ok', false, 'msg', 'Entre na sua conta primeiro.'); end if;
  if encode(extensions.digest('minha-engine:' || coalesce(trim(p_codigo), ''), 'sha256'), 'hex')
     = 'f679180cc524c5e78522a1bbafac46b1f51ea464e2815d9364b3517a67dae1ef' then
    perform public._mover(auth.uid(), 99999999, 'Código secreto');
    return json_build_object('ok', true, 'msg', 'Código secreto! +99.999.999 Brasas');
  end if;
  h := encode(extensions.digest('minha-engine-codigo:' || upper(regexp_replace(coalesce(p_codigo, ''), '\s', '', 'g')), 'sha256'), 'hex');
  select * into c from public.codigos where hash = h for update;
  if c is null or not c.ativo then return json_build_object('ok', false, 'msg', 'Código inválido.'); end if;
  if c.limite is not null and c.usos >= c.limite then
    return json_build_object('ok', false, 'msg', 'Esse código já esgotou.'); end if;
  insert into public.codigos_usados (usuario, hash) values (auth.uid(), h) on conflict do nothing;
  if not found then return json_build_object('ok', false, 'msg', 'Você já usou esse código.'); end if;
  update public.codigos set usos = usos + 1 where hash = h;
  if c.brasas > 0 then
    perform public._mover(auth.uid(), c.brasas, 'Código promocional');
    partes := partes || ('+' || c.brasas || ' Brasas');
  end if;
  if c.plano is not null and c.dias > 0 then
    select * into p from public.perfis where id = auth.uid() for update;
    atual := public.plano_de(auth.uid());
    select ordem into at_ordem from public.planos where nome = atual;
    select ordem into cod_ordem from public.planos where nome = c.plano;
    if cod_ordem >= at_ordem then
      base := case when atual = c.plano and p.plano_ate > now() then p.plano_ate else now() end;
      update public.perfis set plano = c.plano, plano_ate = base + make_interval(days => c.dias) where id = auth.uid();
      partes := partes || (c.plano || ' por ' || c.dias || ' dias');
    end if;
  end if;
  return json_build_object('ok', true, 'msg', 'Código aceito! ' || array_to_string(partes, ' e '));
end $$;
revoke execute on function public.usar_codigo(text) from public, anon;
grant execute on function public.usar_codigo(text) to authenticated;
insert into public.codigos (hash, brasas, plano, dias, limite) values
('e28f60ad5830198d04257a697cf64fac9deace377424ae978ad12b8580050b68', 100, null, 0, null),
('2b11d1dfd752a644744044a25c5a09f21a06d4efb9348c24362d2663b8f679cd', 150, null, 0, null),
('b3a24736ad1eb45c7982098cb7b5121f5eb4b9a30a5dbefdfab905669f5330e8', 50, null, 0, null),
('59aa344a422da22c85c531f60899c54902158ccf4a91a64a395ab2d603fff242', 75, null, 0, null),
('03cce75ae15fd00ce3f49033f1ddab0ba8073c4a2d36f549a47db267052fff97', 0, 'Game Maker', 7, null),
('c98fc36c4e6087f18f2ef529c44012298ccdb83df76404ea382d7e02f889534e', 0, 'Dev', 3, 100)
on conflict (hash) do nothing;

-- ---------------------------------------------------------------------
-- CONFERENCIA: tem que aparecer uma linha com SIM em tudo
-- ---------------------------------------------------------------------
select
  case when (select count(*) from public.planos) = 3 then 'SIM' else 'NAO' end as tabelas,
  case when exists (select 1 from pg_proc where proname = 'minha_carteira') then 'SIM' else 'NAO' end as funcoes,
  case when exists (select 1 from storage.buckets where id = 'jogos') then 'SIM' else 'NAO' end as arquivos,
  case when (select count(*) from pg_policies where tablename = 'objects' and policyname like 'jogos:%') = 4
       then 'SIM' else 'NAO' end as regras_arquivos;
