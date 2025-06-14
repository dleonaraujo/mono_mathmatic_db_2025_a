from django.db import models


class Cursos(models.Model):
    idcurso = models.AutoField(db_column='IdCurso', primary_key=True)  # Field name made lowercase.
    nombrecurso = models.CharField(db_column='NombreCurso', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    precio = models.DecimalField(db_column='Precio', max_digits=10, decimal_places=2)  # Field name made lowercase.
    iddisponibilidadcurso = models.ForeignKey('Disponibilidadcurso', models.DO_NOTHING, db_column='IdDisponibilidadCurso')  # Field name made lowercase.
    idprofesor = models.ForeignKey('Profesores', models.DO_NOTHING, db_column='IdProfesor')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cursos'


class Dia(models.Model):
    iddia = models.AutoField(db_column='IdDia', primary_key=True)  # Field name made lowercase.
    nombredia = models.CharField(db_column='NombreDia', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dia'


class Disponibilidadcurso(models.Model):
    iddisponibilidadcurso = models.AutoField(db_column='IdDisponibilidadCurso', primary_key=True)  # Field name made lowercase.
    disponibilidad = models.BooleanField(db_column='Disponibilidad')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DisponibilidadCurso'


class Disponibilidadhorario(models.Model):
    iddisponibilidadhorario = models.AutoField(db_column='IdDisponibilidadHorario', primary_key=True)  # Field name made lowercase.
    disponibilidad = models.BooleanField(db_column='Disponibilidad')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DisponibilidadHorario'


class Disponibilidadsalon(models.Model):
    iddisponibilidadsalon = models.AutoField(db_column='IdDisponibilidadSalon', primary_key=True)  # Field name made lowercase.
    disponibilidad = models.BooleanField(db_column='Disponibilidad')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DisponibilidadSalon'


class Estudiantes(models.Model):
    idestudiante = models.AutoField(db_column='IdEstudiante', primary_key=True)  # Field name made lowercase.
    nombres = models.CharField(db_column='Nombres', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    apellidopaterno = models.CharField(db_column='ApellidoPaterno', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    apellidomaterno = models.CharField(db_column='ApellidoMaterno', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    telefonoestudiante = models.CharField(db_column='TelefonoEstudiante', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    fechanacimiento = models.DateField(db_column='FechaNacimiento')  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Estudiantes'


class Horario(models.Model):
    idhorario = models.AutoField(db_column='IdHorario', primary_key=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    horainicio = models.TimeField(db_column='HoraInicio')  # Field name made lowercase.
    horafin = models.TimeField(db_column='HoraFin')  # Field name made lowercase.
    iddia = models.ForeignKey(Dia, models.DO_NOTHING, db_column='IdDia')  # Field name made lowercase.
    iddisponibilidadhorario = models.ForeignKey(Disponibilidadhorario, models.DO_NOTHING, db_column='IdDisponibilidadHorario')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Horario'


class Imparte(models.Model):
    idprofesor = models.OneToOneField('Profesores', models.DO_NOTHING, db_column='IdProfesor', primary_key=True)  # Field name made lowercase. The composite primary key (IdProfesor, IdCurso) found, that is not supported. The first column is selected.
    idcurso = models.ForeignKey(Cursos, models.DO_NOTHING, db_column='IdCurso')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Imparte'
        unique_together = (('idprofesor', 'idcurso'),)


class Orden(models.Model):
    idorden = models.AutoField(db_column='IdOrden', primary_key=True)  # Field name made lowercase.
    fechaorden = models.DateField(db_column='FechaOrden')  # Field name made lowercase.
    idestudiante = models.ForeignKey(Estudiantes, models.DO_NOTHING, db_column='IdEstudiante')  # Field name made lowercase.
    idcurso = models.ForeignKey(Cursos, models.DO_NOTHING, db_column='IdCurso')  # Field name made lowercase.
    idsalon = models.ForeignKey('Salones', models.DO_NOTHING, db_column='IdSalon')  # Field name made lowercase.
    idhorario = models.ForeignKey(Horario, models.DO_NOTHING, db_column='IdHorario')  # Field name made lowercase.
    estado = models.BooleanField(db_column='Estado')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Orden'


class Ordenparticionada(models.Model):
    idorden = models.IntegerField(db_column='IdOrden')  # Field name made lowercase.
    fechaorden = models.DateField(db_column='FechaOrden')  # Field name made lowercase.
    idestudiante = models.IntegerField(db_column='IdEstudiante', blank=True, null=True)  # Field name made lowercase.
    idcurso = models.IntegerField(db_column='IdCurso', blank=True, null=True)  # Field name made lowercase.
    idsalon = models.IntegerField(db_column='IdSalon', blank=True, null=True)  # Field name made lowercase.
    idhorario = models.IntegerField(db_column='IdHorario', blank=True, null=True)  # Field name made lowercase.
    estado = models.BooleanField(db_column='Estado', blank=True, null=True)  # Field name made lowercase.
    anio = models.IntegerField(db_column='Anio', primary_key=True)  # Field name made lowercase. The composite primary key (Anio, IdOrden) found, that is not supported. The first column is selected.

    class Meta:
        managed = False
        db_table = 'OrdenParticionada'
        unique_together = (('anio', 'idorden'),)


class Profesores(models.Model):
    idprofesor = models.AutoField(db_column='IdProfesor', primary_key=True)  # Field name made lowercase.
    nombres = models.CharField(db_column='Nombres', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    apellidopaterno = models.CharField(db_column='ApellidoPaterno', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    apellidomaterno = models.CharField(db_column='ApellidoMaterno', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    telefonoprofesor = models.CharField(db_column='TelefonoProfesor', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Profesores'


class Salones(models.Model):
    idsalon = models.AutoField(db_column='IdSalon', primary_key=True)  # Field name made lowercase.
    codigosalon = models.CharField(db_column='CodigoSalon', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    aforosalon = models.IntegerField(db_column='AforoSalon')  # Field name made lowercase.
    iddisponibilidad = models.ForeignKey(Disponibilidadsalon, models.DO_NOTHING, db_column='IdDisponibilidad')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Salones'


class Solicita(models.Model):
    idestudiante = models.OneToOneField(Estudiantes, models.DO_NOTHING, db_column='IdEstudiante', primary_key=True)  # Field name made lowercase. The composite primary key (IdEstudiante, IdCurso) found, that is not supported. The first column is selected.
    idcurso = models.ForeignKey(Cursos, models.DO_NOTHING, db_column='IdCurso')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Solicita'
        unique_together = (('idestudiante', 'idcurso'),)


class Sysdiagrams(models.Model):
    name = models.CharField(max_length=128, db_collation='SQL_Latin1_General_CP1_CI_AS')
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)
