-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 12-06-2020 a las 19:18:02
-- Versión del servidor: 10.4.11-MariaDB
-- Versión de PHP: 7.2.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `Imagym`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Actividad_cardio`
--

CREATE TABLE `Actividad_cardio` (
  `id_actividad_cardio` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `Actividad_cardio`
--

INSERT INTO `Actividad_cardio` (`id_actividad_cardio`, `nombre`) VALUES
(1, 'Cinta de correr'),
(2, 'Elíptica'),
(3, 'Máquinas escaladoras'),
(4, 'Bicicleta estática'),
(5, 'Natación');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Calendario`
--

CREATE TABLE `Calendario` (
  `id_reto` int(11) NOT NULL,
  `dia` int(11) NOT NULL,
  `repeticiones` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `Calendario`
--

INSERT INTO `Calendario` (`id_reto`, `dia`, `repeticiones`) VALUES
(1, 1, '5'),
(1, 2, '10'),
(1, 3, '15'),
(2, 1, '1'),
(2, 2, '2'),
(2, 3, '3'),
(2, 4, '4'),
(2, 5, '5'),
(2, 6, '6'),
(2, 7, '7'),
(2, 8, '8'),
(2, 9, NULL),
(2, 10, '10');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Cardio_en_gimnasio`
--

CREATE TABLE `Cardio_en_gimnasio` (
  `id_gym` int(11) NOT NULL,
  `id_actividad_cardio` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `Cardio_en_gimnasio`
--

INSERT INTO `Cardio_en_gimnasio` (`id_gym`, `id_actividad_cardio`) VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Ejercicios`
--

CREATE TABLE `Ejercicios` (
  `id_ejercicio` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `tipo` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `Ejercicios`
--

INSERT INTO `Ejercicios` (`id_ejercicio`, `nombre`, `tipo`) VALUES
(1, 'Flexiones', 'reto'),
(2, 'Abdominales', 'reto'),
(3, 'Sentadillas', ''),
(4, 'Lunges', ''),
(5, 'Femoral sentado', ''),
(6, 'Femoral tumbado', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Ejercicio_del_mes`
--

CREATE TABLE `Ejercicio_del_mes` (
  `id_objetivo_mensual` int(11) NOT NULL,
  `objetivo` varchar(50) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `date_add` date NOT NULL,
  `id_trainer` int(11) NOT NULL,
  `id_actividad_cardio` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `Ejercicio_del_mes`
--

INSERT INTO `Ejercicio_del_mes` (`id_objetivo_mensual`, `objetivo`, `fecha_inicio`, `fecha_fin`, `date_add`, `id_trainer`, `id_actividad_cardio`) VALUES
(1, '500 minutos', '2020-06-01', '2020-06-30', '2020-06-12', 1, 1),
(2, '500 distancia', '2020-07-01', '2020-07-31', '2020-06-12', 1, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Ejercita`
--

CREATE TABLE `Ejercita` (
  `id_ejercicio` int(11) NOT NULL,
  `id_musculo` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Gimnasios`
--

CREATE TABLE `Gimnasios` (
  `id_gym` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `cif` varchar(9) DEFAULT NULL,
  `telefono` int(11) DEFAULT NULL,
  `clave_admin` varchar(20) NOT NULL,
  `clave_clientes` varchar(20) NOT NULL,
  `caducidad_clave_clientes` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `Gimnasios`
--

INSERT INTO `Gimnasios` (`id_gym`, `nombre`, `cif`, `telefono`, `clave_admin`, `clave_clientes`, `caducidad_clave_clientes`) VALUES
(1, 'Gimnasio Kronos', NULL, NULL, 'admin', 'clientes', '2021-03-04');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Hace_rutina`
--

CREATE TABLE `Hace_rutina` (
  `id_usuario` varchar(20) NOT NULL,
  `id_rutina` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `id_ejercicio` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Musculos`
--

CREATE TABLE `Musculos` (
  `id_musculo` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Objetivo_personal_cardio`
--

CREATE TABLE `Objetivo_personal_cardio` (
  `id_objetivo_personal` int(11) NOT NULL,
  `objetivo` varchar(50) DEFAULT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `estado` varchar(1) NOT NULL,
  `date_add` date NOT NULL,
  `id_usuario` varchar(20) NOT NULL,
  `id_actividad_cardio` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `Objetivo_personal_cardio`
--

INSERT INTO `Objetivo_personal_cardio` (`id_objetivo_personal`, `objetivo`, `fecha_inicio`, `fecha_fin`, `estado`, `date_add`, `id_usuario`, `id_actividad_cardio`) VALUES
(23, '300 minutos', '2020-06-12', '2020-07-12', 'C', '2020-06-12', 'Jumacasni', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Objetivo_peso`
--

CREATE TABLE `Objetivo_peso` (
  `id_objetivo_peso` int(11) NOT NULL,
  `tipo` varchar(7) NOT NULL,
  `objetivo` decimal(10,3) NOT NULL,
  `diferencia` decimal(10,3) DEFAULT NULL,
  `fecha_inicio` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL,
  `date_add` date NOT NULL,
  `id_usuario` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Peso`
--

CREATE TABLE `Peso` (
  `id_peso` int(11) NOT NULL,
  `peso` decimal(10,3) DEFAULT NULL,
  `grasa` decimal(10,3) DEFAULT NULL,
  `musculo` decimal(10,3) DEFAULT NULL,
  `IMC` decimal(10,3) DEFAULT NULL,
  `fecha` date NOT NULL,
  `hora` time NOT NULL,
  `id_usuario` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `Peso`
--

INSERT INTO `Peso` (`id_peso`, `peso`, `grasa`, `musculo`, `IMC`, `fecha`, `hora`, `id_usuario`) VALUES
(25, '98.000', NULL, NULL, '26.860', '2020-06-11', '17:36:03', 'Jumacasni');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Realiza_reto`
--

CREATE TABLE `Realiza_reto` (
  `id_usuario` varchar(20) NOT NULL,
  `id_reto` int(11) NOT NULL,
  `estado` varchar(1) NOT NULL,
  `dia` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `Realiza_reto`
--

INSERT INTO `Realiza_reto` (`id_usuario`, `id_reto`, `estado`, `dia`) VALUES
('Jumacasni', 1, 'A', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Registra_cardio`
--

CREATE TABLE `Registra_cardio` (
  `id_actividad_cardio` int(11) NOT NULL,
  `id_usuario` varchar(20) NOT NULL,
  `fecha` datetime NOT NULL,
  `tiempo` int(11) DEFAULT NULL,
  `distancia` decimal(10,3) DEFAULT NULL,
  `nivel` int(11) DEFAULT NULL,
  `calorias` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `Registra_cardio`
--

INSERT INTO `Registra_cardio` (`id_actividad_cardio`, `id_usuario`, `fecha`, `tiempo`, `distancia`, `nivel`, `calorias`) VALUES
(1, 'Jumacasni', '2020-06-09 11:40:38', 40, NULL, NULL, NULL),
(1, 'Jumacasni', '2020-06-12 13:45:52', NULL, '40.000', NULL, NULL),
(1, 'Jumacasni', '2020-06-12 13:50:41', 15, NULL, NULL, NULL),
(1, 'Jumacasni', '2020-06-12 13:55:12', 20, NULL, NULL, NULL),
(1, 'Jumacasni', '2020-06-12 15:38:01', 500, NULL, NULL, NULL),
(1, 'Jumacasni', '2020-06-12 16:08:04', 20, NULL, NULL, NULL),
(1, 'Jumacasni', '2020-06-12 16:09:25', 20, NULL, NULL, NULL),
(1, 'Jumacasni', '2020-06-12 16:10:52', 20, NULL, NULL, NULL),
(2, 'Jumacasni', '2020-06-12 13:52:51', 30, NULL, NULL, NULL),
(2, 'Jumacasni', '2020-06-12 13:57:16', 30, '40.000', 50, NULL),
(3, 'Jumacasni', '2020-06-12 14:01:58', 30, '40.000', 50, 200),
(3, 'Jumacasni', '2020-06-12 14:02:44', 20, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Retos`
--

CREATE TABLE `Retos` (
  `id_reto` int(11) NOT NULL,
  `nivel` int(11) NOT NULL,
  `fecha_inicio` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL,
  `date_add` date NOT NULL,
  `id_trainer` int(11) NOT NULL,
  `id_ejercicio` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `Retos`
--

INSERT INTO `Retos` (`id_reto`, `nivel`, `fecha_inicio`, `fecha_fin`, `date_add`, `id_trainer`, `id_ejercicio`) VALUES
(1, 2, '2020-06-12', '2020-06-14', '2020-06-10', 1, 1),
(2, 3, '2020-08-01', '2020-09-01', '2020-06-11', 1, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Rutinas`
--

CREATE TABLE `Rutinas` (
  `id_rutina` int(11) NOT NULL,
  `date_add` date NOT NULL,
  `id_trainer` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `Rutinas`
--

INSERT INTO `Rutinas` (`id_rutina`, `date_add`, `id_trainer`) VALUES
(1, '2020-06-12', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Rutinas_ejercicios`
--

CREATE TABLE `Rutinas_ejercicios` (
  `id_rutina` int(11) NOT NULL,
  `id_ejercicio` int(11) NOT NULL,
  `repeticiones` varchar(50) NOT NULL,
  `dia` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `Rutinas_ejercicios`
--

INSERT INTO `Rutinas_ejercicios` (`id_rutina`, `id_ejercicio`, `repeticiones`, `dia`) VALUES
(1, 1, '5x10', '1'),
(1, 1, '4x12', '2'),
(1, 2, '5x10', '3'),
(1, 2, '5x12', '4'),
(1, 3, '4x10', '1'),
(1, 3, '5x12', '4'),
(1, 4, '4x15', '1'),
(1, 5, '4x12', '1'),
(1, 5, '5x12', '4'),
(1, 6, '6x8', '4');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Se_apunta`
--

CREATE TABLE `Se_apunta` (
  `id_usuario` varchar(20) NOT NULL,
  `id_objetivo_mensual` int(11) NOT NULL,
  `estado` varchar(1) NOT NULL,
  `puntuacion` decimal(10,1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `Se_apunta`
--

INSERT INTO `Se_apunta` (`id_usuario`, `id_objetivo_mensual`, `estado`, `puntuacion`) VALUES
('Jumacasni', 1, 'C', '783.5'),
('Jumacasni', 2, 'A', '0.0'),
('lulivi', 1, 'R', '500.0');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Trainers`
--

CREATE TABLE `Trainers` (
  `id_trainer` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellidos` varchar(50) NOT NULL,
  `DNI` varchar(9) NOT NULL,
  `id_gym` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `Trainers`
--

INSERT INTO `Trainers` (`id_trainer`, `nombre`, `apellidos`, `DNI`, `id_gym`) VALUES
(1, 'Juan Manuel', 'Castillo Nievas', '76591779P', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Ubicaciones`
--

CREATE TABLE `Ubicaciones` (
  `id_ubicacion` int(50) NOT NULL,
  `direccion` varchar(50) NOT NULL,
  `ciudad` varchar(50) NOT NULL,
  `provincia` varchar(50) NOT NULL,
  `codigo_postal` int(11) NOT NULL,
  `id_gym` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Usuarios`
--

CREATE TABLE `Usuarios` (
  `id_usuario` varchar(20) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellidos` varchar(50) DEFAULT NULL,
  `chat_id` varchar(50) NOT NULL,
  `clave_web` varchar(20) NOT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `altura` int(11) DEFAULT NULL,
  `genero` varchar(1) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `id_rutina` int(11) DEFAULT NULL,
  `date_add` date NOT NULL,
  `id_gym` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `Usuarios`
--

INSERT INTO `Usuarios` (`id_usuario`, `nombre`, `apellidos`, `chat_id`, `clave_web`, `fecha_nacimiento`, `altura`, `genero`, `email`, `id_rutina`, `date_add`, `id_gym`) VALUES
('Jumacasni', 'Juan Manuel', NULL, '192276362', 'T7ooNKcque', '1997-08-06', 191, NULL, NULL, NULL, '2020-06-04', 1),
('lulivi', 'Luvo', NULL, '7719679', 'DZ2gZDQNdP', NULL, 170, NULL, NULL, NULL, '2020-06-06', 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `Actividad_cardio`
--
ALTER TABLE `Actividad_cardio`
  ADD PRIMARY KEY (`id_actividad_cardio`);

--
-- Indices de la tabla `Calendario`
--
ALTER TABLE `Calendario`
  ADD PRIMARY KEY (`id_reto`,`dia`);

--
-- Indices de la tabla `Cardio_en_gimnasio`
--
ALTER TABLE `Cardio_en_gimnasio`
  ADD PRIMARY KEY (`id_gym`,`id_actividad_cardio`),
  ADD KEY `id_actividad_cardio` (`id_actividad_cardio`);

--
-- Indices de la tabla `Ejercicios`
--
ALTER TABLE `Ejercicios`
  ADD PRIMARY KEY (`id_ejercicio`);

--
-- Indices de la tabla `Ejercicio_del_mes`
--
ALTER TABLE `Ejercicio_del_mes`
  ADD PRIMARY KEY (`id_objetivo_mensual`),
  ADD KEY `id_trainer_fk` (`id_trainer`),
  ADD KEY `id_actividad_cardio_fk` (`id_actividad_cardio`);

--
-- Indices de la tabla `Ejercita`
--
ALTER TABLE `Ejercita`
  ADD PRIMARY KEY (`id_ejercicio`,`id_musculo`),
  ADD KEY `id_musculo_fk` (`id_musculo`);

--
-- Indices de la tabla `Gimnasios`
--
ALTER TABLE `Gimnasios`
  ADD PRIMARY KEY (`id_gym`);

--
-- Indices de la tabla `Hace_rutina`
--
ALTER TABLE `Hace_rutina`
  ADD PRIMARY KEY (`id_usuario`,`id_rutina`,`fecha`,`id_ejercicio`),
  ADD KEY `id_rutina` (`id_rutina`),
  ADD KEY `id_ejercicio` (`id_ejercicio`);

--
-- Indices de la tabla `Musculos`
--
ALTER TABLE `Musculos`
  ADD PRIMARY KEY (`id_musculo`);

--
-- Indices de la tabla `Objetivo_personal_cardio`
--
ALTER TABLE `Objetivo_personal_cardio`
  ADD PRIMARY KEY (`id_objetivo_personal`),
  ADD KEY `id_actividad_cardio` (`id_actividad_cardio`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `Objetivo_peso`
--
ALTER TABLE `Objetivo_peso`
  ADD PRIMARY KEY (`id_objetivo_peso`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `Peso`
--
ALTER TABLE `Peso`
  ADD PRIMARY KEY (`id_peso`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `Realiza_reto`
--
ALTER TABLE `Realiza_reto`
  ADD PRIMARY KEY (`id_usuario`,`id_reto`),
  ADD KEY `id_reto` (`id_reto`);

--
-- Indices de la tabla `Registra_cardio`
--
ALTER TABLE `Registra_cardio`
  ADD PRIMARY KEY (`id_actividad_cardio`,`id_usuario`,`fecha`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `Retos`
--
ALTER TABLE `Retos`
  ADD PRIMARY KEY (`id_reto`),
  ADD KEY `id_ejercicio` (`id_ejercicio`),
  ADD KEY `id_trainer` (`id_trainer`);

--
-- Indices de la tabla `Rutinas`
--
ALTER TABLE `Rutinas`
  ADD PRIMARY KEY (`id_rutina`),
  ADD KEY `id_trainer` (`id_trainer`);

--
-- Indices de la tabla `Rutinas_ejercicios`
--
ALTER TABLE `Rutinas_ejercicios`
  ADD PRIMARY KEY (`id_rutina`,`id_ejercicio`,`dia`),
  ADD KEY `id_ejercicio` (`id_ejercicio`);

--
-- Indices de la tabla `Se_apunta`
--
ALTER TABLE `Se_apunta`
  ADD PRIMARY KEY (`id_usuario`,`id_objetivo_mensual`),
  ADD UNIQUE KEY `id_usuario` (`id_usuario`,`id_objetivo_mensual`),
  ADD KEY `id_objetivo_mensual` (`id_objetivo_mensual`);

--
-- Indices de la tabla `Trainers`
--
ALTER TABLE `Trainers`
  ADD PRIMARY KEY (`id_trainer`),
  ADD KEY `id_gym` (`id_gym`);

--
-- Indices de la tabla `Ubicaciones`
--
ALTER TABLE `Ubicaciones`
  ADD PRIMARY KEY (`id_ubicacion`),
  ADD KEY `id_gym` (`id_gym`);

--
-- Indices de la tabla `Usuarios`
--
ALTER TABLE `Usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD KEY `id_gym` (`id_gym`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `Actividad_cardio`
--
ALTER TABLE `Actividad_cardio`
  MODIFY `id_actividad_cardio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `Ejercicios`
--
ALTER TABLE `Ejercicios`
  MODIFY `id_ejercicio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `Ejercicio_del_mes`
--
ALTER TABLE `Ejercicio_del_mes`
  MODIFY `id_objetivo_mensual` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `Gimnasios`
--
ALTER TABLE `Gimnasios`
  MODIFY `id_gym` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `Musculos`
--
ALTER TABLE `Musculos`
  MODIFY `id_musculo` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `Objetivo_personal_cardio`
--
ALTER TABLE `Objetivo_personal_cardio`
  MODIFY `id_objetivo_personal` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT de la tabla `Objetivo_peso`
--
ALTER TABLE `Objetivo_peso`
  MODIFY `id_objetivo_peso` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `Peso`
--
ALTER TABLE `Peso`
  MODIFY `id_peso` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT de la tabla `Retos`
--
ALTER TABLE `Retos`
  MODIFY `id_reto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `Rutinas`
--
ALTER TABLE `Rutinas`
  MODIFY `id_rutina` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `Trainers`
--
ALTER TABLE `Trainers`
  MODIFY `id_trainer` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `Ubicaciones`
--
ALTER TABLE `Ubicaciones`
  MODIFY `id_ubicacion` int(50) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `Calendario`
--
ALTER TABLE `Calendario`
  ADD CONSTRAINT `Calendario_ibfk_1` FOREIGN KEY (`id_reto`) REFERENCES `Retos` (`id_reto`);

--
-- Filtros para la tabla `Cardio_en_gimnasio`
--
ALTER TABLE `Cardio_en_gimnasio`
  ADD CONSTRAINT `Cardio_en_gimnasio_ibfk_1` FOREIGN KEY (`id_actividad_cardio`) REFERENCES `Actividad_cardio` (`id_actividad_cardio`),
  ADD CONSTRAINT `Cardio_en_gimnasio_ibfk_2` FOREIGN KEY (`id_gym`) REFERENCES `Gimnasios` (`id_gym`);

--
-- Filtros para la tabla `Ejercicio_del_mes`
--
ALTER TABLE `Ejercicio_del_mes`
  ADD CONSTRAINT `id_actividad_cardio_fk` FOREIGN KEY (`id_actividad_cardio`) REFERENCES `Actividad_cardio` (`id_actividad_cardio`),
  ADD CONSTRAINT `id_trainer_fk` FOREIGN KEY (`id_trainer`) REFERENCES `Trainers` (`id_trainer`);

--
-- Filtros para la tabla `Ejercita`
--
ALTER TABLE `Ejercita`
  ADD CONSTRAINT `id_ejercicio_fk` FOREIGN KEY (`id_ejercicio`) REFERENCES `Ejercicios` (`id_ejercicio`),
  ADD CONSTRAINT `id_musculo_fk` FOREIGN KEY (`id_musculo`) REFERENCES `Musculos` (`id_musculo`);

--
-- Filtros para la tabla `Hace_rutina`
--
ALTER TABLE `Hace_rutina`
  ADD CONSTRAINT `Hace_rutina_ibfk_1` FOREIGN KEY (`id_rutina`) REFERENCES `Rutinas` (`id_rutina`),
  ADD CONSTRAINT `Hace_rutina_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `Usuarios` (`id_usuario`),
  ADD CONSTRAINT `Hace_rutina_ibfk_3` FOREIGN KEY (`id_ejercicio`) REFERENCES `Ejercicios` (`id_ejercicio`);

--
-- Filtros para la tabla `Objetivo_personal_cardio`
--
ALTER TABLE `Objetivo_personal_cardio`
  ADD CONSTRAINT `Objetivo_personal_cardio_ibfk_1` FOREIGN KEY (`id_actividad_cardio`) REFERENCES `Actividad_cardio` (`id_actividad_cardio`),
  ADD CONSTRAINT `Objetivo_personal_cardio_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `Usuarios` (`id_usuario`);

--
-- Filtros para la tabla `Objetivo_peso`
--
ALTER TABLE `Objetivo_peso`
  ADD CONSTRAINT `Objetivo_peso_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `Usuarios` (`id_usuario`);

--
-- Filtros para la tabla `Peso`
--
ALTER TABLE `Peso`
  ADD CONSTRAINT `Peso_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `Usuarios` (`id_usuario`);

--
-- Filtros para la tabla `Realiza_reto`
--
ALTER TABLE `Realiza_reto`
  ADD CONSTRAINT `Realiza_reto_ibfk_1` FOREIGN KEY (`id_reto`) REFERENCES `Retos` (`id_reto`),
  ADD CONSTRAINT `Realiza_reto_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `Usuarios` (`id_usuario`);

--
-- Filtros para la tabla `Registra_cardio`
--
ALTER TABLE `Registra_cardio`
  ADD CONSTRAINT `Registra_cardio_ibfk_1` FOREIGN KEY (`id_actividad_cardio`) REFERENCES `Actividad_cardio` (`id_actividad_cardio`),
  ADD CONSTRAINT `Registra_cardio_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `Usuarios` (`id_usuario`);

--
-- Filtros para la tabla `Retos`
--
ALTER TABLE `Retos`
  ADD CONSTRAINT `Retos_ibfk_1` FOREIGN KEY (`id_ejercicio`) REFERENCES `Ejercicios` (`id_ejercicio`),
  ADD CONSTRAINT `Retos_ibfk_2` FOREIGN KEY (`id_trainer`) REFERENCES `Trainers` (`id_trainer`);

--
-- Filtros para la tabla `Rutinas`
--
ALTER TABLE `Rutinas`
  ADD CONSTRAINT `Rutinas_ibfk_1` FOREIGN KEY (`id_trainer`) REFERENCES `Trainers` (`id_trainer`);

--
-- Filtros para la tabla `Rutinas_ejercicios`
--
ALTER TABLE `Rutinas_ejercicios`
  ADD CONSTRAINT `Rutinas_ejercicios_ibfk_1` FOREIGN KEY (`id_ejercicio`) REFERENCES `Ejercicios` (`id_ejercicio`),
  ADD CONSTRAINT `Rutinas_ejercicios_ibfk_2` FOREIGN KEY (`id_rutina`) REFERENCES `Rutinas` (`id_rutina`);

--
-- Filtros para la tabla `Se_apunta`
--
ALTER TABLE `Se_apunta`
  ADD CONSTRAINT `Se_apunta_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `Usuarios` (`id_usuario`),
  ADD CONSTRAINT `Se_apunta_ibfk_2` FOREIGN KEY (`id_objetivo_mensual`) REFERENCES `Ejercicio_del_mes` (`id_objetivo_mensual`);

--
-- Filtros para la tabla `Trainers`
--
ALTER TABLE `Trainers`
  ADD CONSTRAINT `Trainers_ibfk_1` FOREIGN KEY (`id_gym`) REFERENCES `Gimnasios` (`id_gym`);

--
-- Filtros para la tabla `Ubicaciones`
--
ALTER TABLE `Ubicaciones`
  ADD CONSTRAINT `Ubicaciones_ibfk_1` FOREIGN KEY (`id_gym`) REFERENCES `Gimnasios` (`id_gym`);

--
-- Filtros para la tabla `Usuarios`
--
ALTER TABLE `Usuarios`
  ADD CONSTRAINT `Usuarios_ibfk_1` FOREIGN KEY (`id_gym`) REFERENCES `Gimnasios` (`id_gym`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
