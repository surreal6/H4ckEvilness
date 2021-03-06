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
        self.changed = False

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

        self.log_result_mixing(third)

        # print "Control. Changed %s" % (self.changed,)
        self.changed = self.changed or self.are_new_values_to_update(self.diff_urls, third.diff_urls)
        # print "Changed %s %s vs %s" % (self.changed, len(self.diff_urls.keys()), len(third.diff_urls.keys()),)
        self.changed = self.changed or self.are_new_values_to_update(self.names_, third.names_)
        # print "Changed %s" % (self.changed,)
        self.changed = self.changed or self.are_new_values_to_update(self.emails_, third.emails_)
        # print "Changed %s" % (self.changed,)

        self.diff_urls.update(third.diff_urls)
        self.emails_.update(third.emails_)
        self.names_.update(third.names_)

    def populate_name(self):
        self.mix_names()
        final_candidate = None
        final_candidate_value = 0
        for key, value in self.names_.iteritems():
            if value > final_candidate_value:
                final_candidate = key
                final_candidate_value = value
        if not self.name or (self.name is not final_candidate):
            self.name = final_candidate
            # print "Final name %s" % (self.name,)
            self.changed = True

    def get_user_values(self, user_id=None):
        maindb = MainDB()
        return maindb.get_user(self, user_id=user_id)

    @staticmethod
    def are_new_values_to_update(dictA, dictB):
        sym_diff = len(set(dictA.keys()).symmetric_difference(set(dictB.keys())))
        # print "\t Sym.Diff values %s" % (sym_diff,)
        return sym_diff is not 0

    def log_result_mixing(self, third):
        if self.are_new_values_to_update(self.diff_urls, third.diff_urls):
            intersect = set(self.diff_urls.keys()).symmetric_difference(set(third.diff_urls.keys()))
            print "\t [+] %s new %s urls's candidates" % (len(intersect), self.__class__.__name__)
        if self.are_new_values_to_update(self.names_, third.names_):
            intersect = set(self.names_.keys()).symmetric_difference(set(third.names_.keys()))
            print "\t [+] %s new %s name's candidates" % (len(intersect), self.__class__.__name__)
        if self.are_new_values_to_update(self.emails_, third.emails_):
            intersect = set(self.emails_.keys()).symmetric_difference(set(third.emails_.keys()))
            print "\t [+] %s new %s email's candidates" % (len(intersect), self.__class__.__name__)

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
                            # del self.names_[keyB]
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
