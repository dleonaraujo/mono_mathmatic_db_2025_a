from django.db import models


class Cursos(models.Model):
    idcurso = models.AutoField(primary_key=True)
    nombrecurso = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    iddisponibilidadcurso = models.ForeignKey('Disponibilidadcurso', models.DO_NOTHING, null=True, blank=True)
    idprofesor = models.ForeignKey('Profesores', models.DO_NOTHING, null=True, blank=True)

    class Meta:
        db_table = 'Cursos'


class Dia(models.Model):
    iddia = models.AutoField(primary_key=True)
    nombredia = models.CharField(max_length=50)

    class Meta:
        db_table = 'Dia'


class Disponibilidadcurso(models.Model):
    iddisponibilidadcurso = models.AutoField(primary_key=True)
    disponibilidad = models.BooleanField()

    class Meta:
        db_table = 'DisponibilidadCurso'


class Disponibilidadhorario(models.Model):
    iddisponibilidadhorario = models.AutoField(primary_key=True)
    disponibilidad = models.BooleanField()

    class Meta:
        db_table = 'DisponibilidadHorario'


class Disponibilidadsalon(models.Model):
    iddisponibilidadsalon = models.AutoField(primary_key=True)
    disponibilidad = models.BooleanField()

    class Meta:
        db_table = 'DisponibilidadSalon'


class Estudiantes(models.Model):
    idestudiante = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=100)
    apellidopaterno = models.CharField(max_length=100)
    apellidomaterno = models.CharField(max_length=100)
    telefonoestudiante = models.CharField(max_length=15)
    fechanacimiento = models.DateField()
    email = models.CharField(max_length=150, null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'Estudiantes'


class Horario(models.Model):
    idhorario = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=200, null=True, blank=True)
    horainicio = models.TimeField()
    horafin = models.TimeField()
    iddia = models.ForeignKey(Dia, models.DO_NOTHING, null=True, blank=True)
    iddisponibilidadhorario = models.ForeignKey(Disponibilidadhorario, models.DO_NOTHING, null=True, blank=True)

    class Meta:
        db_table = 'Horario'


class Imparte(models.Model):
    idprofesor = models.OneToOneField('Profesores', models.DO_NOTHING, primary_key=True)
    idcurso = models.ForeignKey(Cursos, models.DO_NOTHING, default=1)

    class Meta:
        db_table = 'Imparte'
        unique_together = (('idprofesor', 'idcurso'),)


class Orden(models.Model):
    idorden = models.AutoField(primary_key=True)
    fechaorden = models.DateField()
    idestudiante = models.ForeignKey(Estudiantes, models.DO_NOTHING, null=True, blank=True)
    idcurso = models.ForeignKey(Cursos, models.DO_NOTHING, null=True, blank=True)
    idsalon = models.ForeignKey('Salones', models.DO_NOTHING, null=True, blank=True)
    idhorario = models.ForeignKey(Horario, models.DO_NOTHING, null=True, blank=True)
    estado = models.BooleanField()

    class Meta:
        db_table = 'Orden'


class Ordenparticionada(models.Model):
    idorden = models.IntegerField()
    fechaorden = models.DateField()
    idestudiante = models.IntegerField(null=True, blank=True)
    idcurso = models.IntegerField(null=True, blank=True)
    idsalon = models.IntegerField(null=True, blank=True)
    idhorario = models.IntegerField(null=True, blank=True)
    estado = models.BooleanField(null=True, blank=True)
    anio = models.IntegerField(primary_key=True)

    class Meta:
        db_table = 'OrdenParticionada'
        unique_together = (('anio', 'idorden'),)


class Profesores(models.Model):
    idprofesor = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=100)
    apellidopaterno = models.CharField(max_length=100)
    apellidomaterno = models.CharField(max_length=100)
    telefonoprofesor = models.CharField(max_length=15)

    class Meta:
        db_table = 'Profesores'


class Salones(models.Model):
    idsalon = models.AutoField(primary_key=True)
    codigosalon = models.CharField(max_length=50)
    aforosalon = models.IntegerField()
    iddisponibilidad = models.ForeignKey(Disponibilidadsalon, models.DO_NOTHING, null=True, blank=True)

    class Meta:
        db_table = 'Salones'


class Solicita(models.Model):
    idestudiante = models.OneToOneField(Estudiantes, models.DO_NOTHING, primary_key=True)
    idcurso = models.ForeignKey(Cursos, models.DO_NOTHING, null=True, blank=True)


    class Meta:
        db_table = 'Solicita'
        unique_together = (('idestudiante', 'idcurso'),)


class Sysdiagrams(models.Model):
    name = models.CharField(max_length=128)
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(null=True, blank=True)
    definition = models.BinaryField(null=True, blank=True)

    class Meta:
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)
