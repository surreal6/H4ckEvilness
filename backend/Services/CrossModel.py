from Metas.DbFieldsReading import DbFieldsReading
from Utils.functions import remove_accents
from databases.mainDb import MainDB
from Levenshtein import *


class CrossModel(DbFieldsReading):

    email = None
    email_prefix = None
    name = None
    phone = None
    photo = None
    national_id = None
    names_ = {}
    emails_ = {}
    diff_urls = {}
    _user_fields = ('email', 'name')

    def __init__(self, user_id=None):
        super(CrossModel, self).__init__()
        if user_id:
            pass
        self.diff_urls = dict()
        self.emails_ = dict()
        self.names_ = dict()
        pass

    def __setattr__(self, name, value):
        if name is "email":
            self.__dict__[name] = value
            self.email_prefix = value.split("@")[0]
        else:
            super(CrossModel, self).__setattr__(name, value)

    def put_name_candidate(self, key):
        if self.names_.get(key, 0) is 0:
            for key_in, value in self.names_.iteritems():
                pass
                # print key + " vs " + key_in + "==" + str(jaro(key, key_in))
        self.names_[key] = self.names_.get(key, 0) + 1

    def put_candidate(self, key):
        if self.diff_urls.get(key, 0) is 0:
            pass
            #TODO. Edit distance case
            # print jaro('Thorkel', 'Thorgier')
        self.diff_urls[key] = self.diff_urls.get(key, 0) + 1

    def mix_results(self, third):
        self.diff_urls.update(third.diff_urls)
        self.emails_.update(third.emails_)
        self.names_.update(third.names_)

    def mix_names(self):
        # HINT. Not efficient. Not at all.
        new_names_ = {}
        # print "Candidate len: " + str(len(self.names_))
        # print "Candidate names: " + str(self.names_)
        completeLoop = False
        while not completeLoop:
            for key, value in self.names_.iteritems():
                match = False
                for keyB, valueB in self.names_.iteritems():
                    if self.names_.keys().index(keyB) > self.names_.keys().index(key):
                        nameA = remove_accents(key)
                        nameB = remove_accents(keyB)

                        jaro_rslt = jaro_winkler(nameA, nameB)
                        # print nameA + " vs " + nameA + " == " + str(jaro_rslt)
                        if jaro_rslt > 0.8:
                            self.names_[key] += valueB
                            value += valueB
                            del self.names_[keyB]
                            match = True
                            break
                        else:
                            nameA = remove_accents("Jose Luis Perez Rey")
                            nameB = remove_accents("Pepe Perez Rey")
                            name_atoms = nameA.split(' ')
                            name_atoms_b = nameB.split(' ')
                            for i in range(0, max(len(name_atoms), len(name_atoms_b))):
                                try:
                                    atomA = remove_accents(name_atoms[i])
                                    atomB = remove_accents(name_atoms_b[i])
                                    jaro_rslt_atoms = jaro(atomA, atomB)
                                    jaro_rslt_atoms_w = jaro_winkler(atomA, atomB)
                                    # print atomA + " vs " + atomB + "==" + str(jaro_rslt_atoms)
                                    # print atomA + " vs " + atomB + "==" + str(jaro_rslt_atoms_w)
                                except IndexError:
                                    pass
                            # print str(name_atoms)
                            # print str(name_atoms_b)
                if match:
                    break
            completeLoop = True
        # print "_Candidate len: " + str(len(self.names_))
        # print "_Candidate names: " + str(self.names_)

    def populate_name(self):
        self.mix_names()
        final_candidate = None
        final_candidate_value = 0
        for key, value in self.names_.iteritems():
            if value > final_candidate_value:
                final_candidate = key
                final_candidate_value = value
        self.name = final_candidate
        if self.name:
            pass
            # print "** Name> "+self.name +"("+str(final_candidate_value)+")"

    def get_user_values(self, user_id=None):
        maindb = MainDB()
        return maindb.get_user(self, user_id=user_id)