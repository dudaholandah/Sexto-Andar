create database sextoandar;
use sextoandar;

drop database sextoandar;

create table endereco (
	codigo int primary key not null auto_increment,
	CEP varchar(8) not null,
    rua varchar(30) not null,
    bairro varchar(30) not null,
    cidade varchar(30) not null,
    numero int not null,
    complemento varchar(30) not null
);

create table login(
	codigo int primary key not null auto_increment,
	email varchar(30) not null unique,
    senha varchar(256) not null
);

# atributo multivalorado
create table permissao(
	fk_login int not null,
    # admininistrador, cliente, proprietario, corretor 
    tipo varchar(30) not null,
    foreign key (fk_login) references login(codigo)
    on delete cascade
    on update cascade
);

create table cliente (
	cpf varchar(11) primary key not null,
    nome varchar(50) not null,
    data_de_nascimento date not null,
    sexo varchar(10) not null,
    fk_endereco int not null,
    foreign key (fk_endereco) references endereco(codigo)
    on delete cascade
    on update cascade
);

create table proprietario(
	cpf varchar(11) primary key not null,
    nome varchar(50) not null,
    data_de_nascimento date not null,
    sexo varchar(10) not null,
    fk_endereco int not null,
    foreign key (fk_endereco) references endereco(codigo)
	on delete cascade
    on update cascade
);

create table categoria(
	codigo int primary key not null auto_increment,
    descricao varchar(100) not null
);

create table precos(
	codigo int not null primary key auto_increment,
	aluguel float not null,
    condominio float not null,
    iptu float not null,
    taxas float not null, 
    total float not null
);

create table caracteristicas(
	codigo int not null primary key auto_increment,
	descricao varchar(100) not null,
    quantidade_de_quartos int not null,
    quantidade_de_banheiros int not null,
    quantidade_de_suites int not null,
    area int not null,
    vaga_garagem int not null
);

create table imovel(
	codigo int primary key not null auto_increment,
    fk_endereco int not null,
    foreign key (fk_endereco) references endereco(codigo)
	on delete cascade
    on update cascade,
    fk_proprietario varchar(11) not null,
    foreign key (fk_proprietario) references proprietario(cpf)
	on delete cascade
    on update cascade,
    fk_categoria int not null,
    foreign key (fk_categoria) references categoria(codigo)
	on delete cascade
    on update cascade,
    fk_cliente varchar(11),
    foreign key (fk_cliente) references cliente(cpf)
	on delete cascade
    on update cascade,
    fk_preco int not null,
    foreign key (fk_preco) references precos(codigo)
	on delete cascade
    on update cascade,
    situacao varchar(20) not null,
    fk_caracteristicas int not null,
    foreign key (fk_caracteristicas) references caracteristicas(codigo)
	on delete cascade
    on update cascade
);

create table corretor(
	cpf varchar(11) primary key not null,
    nome varchar(50) not null,
    data_de_nascimento date not null,
    sexo varchar(10) not null,
    fk_endereco int not null,
    foreign key (fk_endereco) references endereco(codigo)
	on delete cascade
    on update cascade,
    horario_trabalho_inicio time not null,
    horario_trabalho_final time not null
);

create table visita(
	codigo int not null primary key auto_increment,
    fk_corretor varchar(11) not null,
    foreign key (fk_corretor) references corretor(cpf)
    on delete cascade
    on update cascade,
    fk_imovel int not null,
    foreign key (fk_imovel) references imovel(codigo)
	on delete cascade
    on update cascade,
    fk_cliente varchar(11) not null,
    foreign key (fk_cliente) references cliente(cpf)
	on delete cascade
    on update cascade,
    dia_horario datetime not null
);

create table fotos(
	codigo int not null primary key auto_increment,
    fk_imovel int not null,
    foreign key (fk_imovel) references imovel(codigo)
	on delete cascade
    on update cascade,
    foto blob not null,
    data_foto date not null,
    descricao varchar(30)
);

create table contrato(
	numero_contrato int not null primary key auto_increment,
	fk_imovel int not null,
    foreign key (fk_imovel) references imovel(codigo)
	on delete cascade
    on update cascade,
	fk_corretor varchar(11) not null,
    foreign key (fk_corretor) references corretor(cpf)
	on delete cascade
    on update cascade,
	fk_cliente varchar(11) not null,
    foreign key (fk_cliente) references cliente(cpf)
	on delete cascade
    on update cascade,
    fk_preco int not null,
    foreign key (fk_preco) references precos(codigo)
	on delete cascade
    on update cascade,
    forma_de_pagamento varchar(20) not null,
    duracao_meses int not null
);

select * from login;
select * from permissao;
select * from endereco;
select * from corretor;
select * from cliente;
select * from proprietario;