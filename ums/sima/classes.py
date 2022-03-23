from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import ARRAY, JSON, INTEGER, SMALLINT, VARCHAR, TEXT, NUMERIC, TIME, BOOLEAN

Base = declarative_base()

class Program(Base):
    __tablename__ = 'programs'
    ID = Column(INTEGER, primary_key=True, index=True, unique=True)

    name = Column(VARCHAR(128), nullable=False, index=True)
    author = Column(VARCHAR(64), nullable=False, index=True)
    describe = Column(TEXT, nullable=True)
    
    marker = Column(VARCHAR(8))
    size1 = Column(NUMERIC(3, 1), default=9)
    size2 = Column(NUMERIC(3, 1), default=7)
    size3 = Column(NUMERIC(3, 1), default=5)
    def_obs_period = Column(NUMERIC(3, 1), default=12)

    def as_list(self):
        return (self.ID, self.name, self.author, self.marker, self.size1, self.size2, self.size3, self.def_obs_period)

    def __str__(self):
        return f"[{self.ID:02d}] {self.name} ({self.author}) '{self.marker}'"
        
    def __repr__(self):
        return f"<Program(ID={self.ID}, name={self.name}, author={self.author}>"
    
    # def __str__(self):
    #     return f"{self.ID} | {self.author} | {self.name}"

class ObservationObject(Base):  
    __tablename__ = 'objects'
    ID = Column(INTEGER, primary_key=True, index=True, unique=True)

    _Program = Column(INTEGER, ForeignKey('programs.ID'), default=1, index=True)
    type = Column(VARCHAR(1), index=True)

    main_id = Column(VARCHAR(32), nullable=False, index=True)
    name_list = Column(ARRAY(VARCHAR(32)), nullable=False)

    ra_2000 = Column(VARCHAR(16))
    dec_2000 = Column(VARCHAR(16))
    ra_2000_f = Column(NUMERIC(9, 6), nullable=True, index=True)
    dec_2000_f = Column(NUMERIC(10, 6), nullable=True, index=True)
    ra_pm = Column(NUMERIC(8, 3), nullable=True, default=None)
    dec_pm = Column(NUMERIC(8, 3), nullable=True, default=None)

    gmag = Column(NUMERIC(4, 2), nullable=True, default=None)
    bmag = Column(NUMERIC(4, 2), nullable=True, default=None)
    vmag = Column(NUMERIC(4, 2), nullable=True, default=None)
    rmag = Column(NUMERIC(4, 2), nullable=True, default=None)
    imag = Column(NUMERIC(4, 2), nullable=True, default=None)
    jmag = Column(NUMERIC(4, 2), nullable=True, default=None)
    hmag = Column(NUMERIC(4, 2), nullable=True, default=None)
    kmag = Column(NUMERIC(4, 2), nullable=True, default=None)

    sptype = Column(VARCHAR(32), nullable=True, default=None)
    parallax = Column(NUMERIC(7, 4), nullable=True, default=None)
    period = Column(NUMERIC(7, 4), nullable=True, default=None)

    status = Column(BOOLEAN, index=True)

    describe = Column(TEXT, nullable=True)

    posN = Column(SMALLINT, default=0)
    orbN = Column(SMALLINT, default=0)
    
    def as_list(self):
        return (self.ID, self._Program, self.t, self.main_name, self.ra_2000, self.dec_2000, self.ra_pm, self.dec_pm,
        self.gmag, self.bmag, self.vmag, self.rmag, self.imag, self.jmag, self.hmag,
        self.sptype, self.parallax, self.period, self.status, self.posN, self.orbN)
    
    # def return_radeg(self):
    #     ra_txt = self.ra_2000
    #     ra_h, ra_m, ra_s = ra_txt.split()
    #     radeg = 15*(float(ra_h) + float(ra_m)/60 + float(ra_s)/3600)
    #     return radeg

    # def return_decdeg(self):
    #     dec_txt = self.dec_2000
    #     dec_d, dec_m, dec_s = dec_txt.split()
    #     decdeg = (-1 if float(dec_d) < 0 else 1) * (abs(float(dec_d)) + float(dec_m) / 60 + float(dec_s) / 3600)
    #     return decdeg
    
    def update_counters(self, session):
        self.posN = session.query(PositionParameter).filter(PositionParameter._Object == self.ID).count()
        self.orbN = session.query(Orbit).filter(Orbit._Object == self.ID).count()

class Orbit(Base):
    __tablename__ = 'orbits'

    ID = Column(INTEGER, primary_key=True, index=True, unique=True)
    
    _Object = Column(INTEGER, ForeignKey('objects.ID'), nullable=False)
    
    type = Column(VARCHAR(16), nullable=False, default='Prepublished')

    P = Column(NUMERIC(7, 4), nullable=False)
    T0 = Column(NUMERIC(8, 4), nullable=False)
    a = Column(NUMERIC(8, 4), nullable=False)
    e = Column(NUMERIC(5, 4), nullable=False)
    W = Column(NUMERIC(7, 4), nullable=False)
    w = Column(NUMERIC(7, 4), nullable=False)
    i = Column(NUMERIC(7, 4), nullable=False)

    P_err = Column(NUMERIC(6, 4), nullable=True)
    T0_err = Column(NUMERIC(6, 4), nullable=True)
    a_err = Column(NUMERIC(6, 4), nullable=True)
    e_err = Column(NUMERIC(6, 4), nullable=True)
    W_err = Column(NUMERIC(6, 4), nullable=True)
    w_err = Column(NUMERIC(6, 4), nullable=True)
    i_err = Column(NUMERIC(6, 4), nullable=True)

    first_author = Column(VARCHAR(16))
    author = Column(TEXT)
    title = Column(VARCHAR(256))
    year = Column(SMALLINT)
    journal = Column(VARCHAR(256))
    doi = Column(VARCHAR(128))
    comment = Column(TEXT)

    def return_list(self):
        return (self.ID, self.t, self.P, self.P_err, self.T0, self.T0_err, self.e, self.e_err, self.a, self.a_err,
                self.W, self.W_err, self.w, self.w_err, self.i, self.i_err, self.author, self.title, self.year, self.journal, self.doi)

class PositionParameter(Base):
    __tablename__ = 'position_parameters'
    ID = Column(INTEGER, primary_key=True, index=True, unique=True)
    _Object = Column(INTEGER, ForeignKey('objects.ID'), nullable=False)

    type = Column(VARCHAR(16), nullable=False, default='Prepublished', index=True)

    epoch = Column(NUMERIC(10, 6), nullable=False)
    rho   = Column(NUMERIC(8, 4), nullable=False)
    rho_err = Column(NUMERIC(6, 4), nullable=True)
    theta = Column(NUMERIC(7, 4), nullable=False)
    theta_err = Column(NUMERIC(6, 4), nullable=True)
    theta_ambiguity = Column(BOOLEAN, default=False)
    dm = Column(NUMERIC(5, 3), nullable=True)
    dm_err = Column(NUMERIC(4, 3), nullable=True)
    filter = Column(VARCHAR(16))

    first_author = Column(VARCHAR(16), nullable=False, index=True)
    author = Column(TEXT, nullable=True)
    title = Column(VARCHAR(256), nullable=True)
    year = Column(SMALLINT, nullable=True)
    journal = Column(VARCHAR(256), nullable=True)
    doi = Column(VARCHAR(128), nullable=True)
    comment = Column(TEXT, nullable=True)

    def return_list(self):
        return self.ID, self.t, self.epoch, self.rho, self.rho_err, self.theta, self.theta_err, self.theta_ambiguity, self.dm, self.dm_err, self.filt, self.author, self.title, self.year, self.journal, self.doi
        
class Journal(Base):
    __tablename__ = 'journal'
    ID = Column(INTEGER, primary_key=True, index=True, unique=True)
    _Object = Column(INTEGER, ForeignKey('objects.ID'))
    
    ra_start = Column(VARCHAR(16))
    dec_start = Column(VARCHAR(16))
    utc_date_start = Column(DateTime)
    lst_date_start = Column(TIME)
    z_start = Column(NUMERIC(4, 2))
    par_ang_start = Column(NUMERIC(5, 2))

    ra_end = Column(VARCHAR(16))
    dec_end = Column(VARCHAR(16))
    utc_date_end = Column(DateTime)
    lst_date_end = Column(TIME)    
    z_end = Column(NUMERIC(4, 2))
    par_ang_end = Column(NUMERIC(5, 2))

    filt = Column(VARCHAR(16))
    gain = Column(SMALLINT)
    mag = Column(SMALLINT)

    focus = Column(NUMERIC(5, 2))

    par_ang_mean = Column(NUMERIC(5, 2))

    t_in = Column(NUMERIC(4, 1))
    t_out = Column(NUMERIC(4, 1))
    t_mir = Column(NUMERIC(4, 1))
    press = Column(NUMERIC(4, 1))
    wind = Column(NUMERIC(4, 2))

    comment = Column(TEXT)
    lines = Column(TEXT)

    def return_list(self):
        return [self.ID, self.lines.split()[0], self.ra_start, self.dec_start, self.utc_date_start, self.lst_date_start, self.par_ang_mean, self.filt, self.gain, self.mag, self.focus, self.comment]

class JournalNameEqual(Base):
    __tablename__ = 'journal_name_equal'
    ID = Column(INTEGER, primary_key=True, index=True, unique=True)
    _Object = Column(INTEGER, ForeignKey('objects.ID'))
    journal_line = Column(TEXT)
    params = Column(JSON)

class AccessLevel(Base):
    __tablename__ = 'gui_access_level'
    ID = Column(INTEGER, primary_key=True)
    login = Column(VARCHAR(16), index=True)
    password = Column(VARCHAR(32))
    level = Column(SMALLINT)