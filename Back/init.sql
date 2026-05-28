CREATE TABLE IF NOT EXISTS USUARIO (
  id_usuario     INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nombre         VARCHAR(100) NOT NULL,
  apellidos      VARCHAR(150),
  email          VARCHAR(255) NOT NULL UNIQUE,
  contrasena     VARCHAR(255) NOT NULL,
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS OFERTA_EMPLEO (
  id_oferta    INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  titulo       VARCHAR(255),
  empresa      VARCHAR(255),
  descripcion  TEXT,
  requisitos   TEXT
);

CREATE TABLE IF NOT EXISTS CURRICULUM (
  id_cv          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  id_usuario     INT UNSIGNED NOT NULL,
  id_oferta      INT UNSIGNED,
  titulo         VARCHAR(255),
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  hash_control   VARCHAR(64),
  tiene_foto     TINYINT(1) DEFAULT 0,
  plantilla      VARCHAR(20) DEFAULT 'europass',
  descripcion    TEXT,
  porcentaje     TINYINT UNSIGNED,

  CONSTRAINT fk_cv_usuario 
    FOREIGN KEY (id_usuario) 
    REFERENCES USUARIO(id_usuario) 
    ON DELETE CASCADE,

  CONSTRAINT fk_cv_oferta  
    FOREIGN KEY (id_oferta)  
    REFERENCES OFERTA_EMPLEO(id_oferta) 
    ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS DATOS_PERSONALES (
  id_datos         INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  id_cv            INT UNSIGNED NOT NULL UNIQUE,
  nombre           VARCHAR(100),
  apellido         VARCHAR(100),
  email            VARCHAR(100),
  telefono         VARCHAR(20),
  direccion        VARCHAR(255),
  codigo_postal    VARCHAR(10),
  localidad        VARCHAR(100),
  permiso_conducir TINYINT(1) DEFAULT 0,

  CONSTRAINT fk_datos_cv 
    FOREIGN KEY (id_cv) 
    REFERENCES CURRICULUM(id_cv) 
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS EXPERIENCIA_LABORAL (
  id_experiencia INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  id_cv          INT UNSIGNED NOT NULL,
  empresa        VARCHAR(255),
  puesto         VARCHAR(255),
  fecha_inicio   VARCHAR(50),
  fecha_fin      VARCHAR(50),
  descripcion    TEXT,

  CONSTRAINT fk_exp_cv 
    FOREIGN KEY (id_cv) 
    REFERENCES CURRICULUM(id_cv) 
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS EDUCACION (
  id_educacion INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  id_cv        INT UNSIGNED NOT NULL,
  institucion  VARCHAR(255),
  titulo       VARCHAR(255),
  anioInicio   VARCHAR(50),
  anioFin      VARCHAR(50),

  CONSTRAINT fk_edu_cv 
    FOREIGN KEY (id_cv) 
    REFERENCES CURRICULUM(id_cv) 
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS CERTIFICACION (
  id_certificacion INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  id_cv            INT UNSIGNED NOT NULL,
  certificacion    VARCHAR(255),
  expedicion       VARCHAR(50),

  CONSTRAINT fk_cert_cv 
    FOREIGN KEY (id_cv) 
    REFERENCES CURRICULUM(id_cv) 
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS IDIOMA (
  id_idioma INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  id_cv     INT UNSIGNED NOT NULL,
  nombre    VARCHAR(100),
  nivel     ENUM('Básico','Intermedio','Avanzado','Nativo') DEFAULT 'Básico',

  CONSTRAINT fk_idioma_cv 
    FOREIGN KEY (id_cv) 
    REFERENCES CURRICULUM(id_cv) 
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS HABILIDAD (
  id_habilidad INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nombre       VARCHAR(150) UNIQUE
);

CREATE TABLE IF NOT EXISTS CV_HABILIDAD (
  id_cv        INT UNSIGNED NOT NULL,
  id_habilidad INT UNSIGNED NOT NULL,

  PRIMARY KEY (id_cv, id_habilidad),

  CONSTRAINT fk_cvh_cv        
    FOREIGN KEY (id_cv)        
    REFERENCES CURRICULUM(id_cv) 
    ON DELETE CASCADE,

  CONSTRAINT fk_cvh_habilidad 
    FOREIGN KEY (id_habilidad) 
    REFERENCES HABILIDAD(id_habilidad) 
    ON DELETE CASCADE
);