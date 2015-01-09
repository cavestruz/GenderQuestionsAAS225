import csv
import numpy as np
csvfilename = '../data/survey_responses.csv'

class GenderSurveyQuestions : 
    '''This class reads in the survey responses csv file, normalizes
    all of the responses, then puts all of the responses into
    dictionaries that can easily be called for analysis. The csv file
    should have no header.'''
    
    def __init__( self, gendercsv ) :

        self.fields = ['time_stamp','status', 'gender', 'have_asked', 'hesitated',
                  'why_not', 'why_do', 'recommendations', 'free_response']
        self.indices = {}
        self.shortwhys = ['unimportant', 'repeat', 'unnoticed', 'far seat',
        'nervous', 'stupid question', 'questions unimportant',
        'nothing worthwhile', 'tweeting']
        

        self._read_csv( gendercsv ) 
        self._responses_in_nparrays()
        self._get_ind()

    def _get_ind( self ) :
        '''Get various indices for each question's answer'''
        
        # Gender
        self.indices['M'] = np.where(self.responses_dict['gender'] == 'M')
        self.indices['F'] = np.where(self.responses_dict['gender'] == 'F')

        # Status
        self.indices['academic'] = np.where(self.responses_dict['status'] == 'academic')
        self.indices['grad'] = np.where(self.responses_dict['status'] == 'grad')
        self.indices['postdoc'] = np.where(self.responses_dict['status'] == 'postdoc')
        self.indices['educator'] = np.where(self.responses_dict['status'] == 'educator')
        self.indices['industry'] = np.where(self.responses_dict['status'] == 'industry')
        self.indices['Between'] = np.where(self.responses_dict['status'] == 'Between')

        # Asked question
        self.indices['have asked'] = np.where(self.responses_dict['have_asked'] == 'Y')
        self.indices['never asked'] = np.where(self.responses_dict['have_asked'] == 'N')

        # Wanted to ask question
        self.indices['hesitated'] = np.where(self.responses_dict['hesitated'] == 'Y')
        self.indices['never hesitated'] = np.where(self.responses_dict['hesitated'] == 'N')

        # Reasons for not asking
        for sw in self.shortwhys : 
            self.indices[sw] = np.where(self.responses_dict[sw] == 'Y')


    def _responses_in_nparrays(self) : 
        '''Turns all of the values in the self.responses_dict from a
        list to a numpy array.'''

        for k, v in self.responses_dict.iteritems() :
            self.responses_dict[k] = np.array(v)

    def _read_csv(self, gendercsv ) :
        '''Reads CSV file and separates into 9 rows.  Creates dictionary
        with each response as a key, and values are numpy files'''

        self.responses_dict = { field: [] for field in self.fields}
        self.responses_dict.update({ field : [] for field in
                                    self.shortwhys })

        with open(csvfilename) as csvfile:
            # responses is an iterable that iterates over each
            # responder returning a list of their responses
            responses = csv.reader(csvfile, delimiter=',', quotechar='"')
            for response in responses :
                dictionary_entry = dict( zip(self.fields, response) ) 
                self._normalize_entry(dictionary_entry)

    def _normalize_entry( self, entry ) :
        '''Normalizes the responses and the academic status responses.
        This expects an entry that is a dictionary, searches for one
        of the entries, and appends to the self.responses dictionary'''
        self._normalize_gender(entry)
        self._normalize_status(entry) 
        self._normalize_asked_qq(entry)
        self._normalize_wanted_qq(entry)
        self._normalize_why_not(entry)

    def _normalize_gender( self, entry ) :
        '''Check gender, normalize, append'''

        femaletrue = entry['gender'].startswith('F') or \
            entry['gender'].startswith('f') or \
            'f' in entry['gender'] or 'F' in entry['gender'] or \
            'W' in entry['gender']
        if femaletrue:                                                                  
            self.responses_dict['gender'].append('F')                                                                            
        else:                                                                  
            self.responses_dict['gender'].append('M')         

    
    def _normalize_status( self, entry ) :
        ''' Check status, normalize, append'''

        shortstatus = entry['status'].split()[0]
        self.responses_dict['status'].append(shortstatus)

    def _normalize_asked_qq( self, entry ) :
        '''Change to Y or N'''
        self.responses_dict['have_asked'].append(entry['have_asked'][0])
        
    def _normalize_wanted_qq( self, entry ) :
        ''' Change to Y or N '''
        self.responses_dict['hesitated'].append(entry['hesitated'][0])

    def _normalize_why_not( self, entry ) :
        '''The why not entry may have multiple ones'''
        searchwhys = ['important enough', 'already', 'noticed', 'far',
                     'nervous', 'stupid', 'questions is important', 'worthwhile',
                     'tweeting'] 
        
        ### Create this into why/whynot dict with Y and N... ###
        # self.shortwhys
        for whynot in entry['why_not'].split(',') : 
            print "Why not: ", whynot
            # Check if each entry has one of these answers
            for sw in searchwhys : 
                swindex = searchwhys.index(sw)
                if sw in whynot : 
                    self.responses_dict[self.shortwhys[swindex]].append('Y')
                else : 
                    self.responses_dict[self.shortwhys[swindex]].append('N')

    def get_number_options( self ) :
        '''Finds keys that one can find the number of people who
        responded with a given answer'''

        return self.indices.keys()

    def get_number( self, key ) :
        '''Gets the number of people who answered something.'''

        return len(self.indices[key][0])

    def gender_split( self ) :
        ''' Returns number of responses from each gender as {'M':
        <int>, 'F': <int>} '''
        
        return {'M': self.get_number('M'), 'F': self.get_number('F')}

    def _intersect_lists( self, a, b ) :
        '''Finds intersectionof two lists a and b'''
        return list(set(a) & set(b))

    def get_number_overlap( self, key1, key2 ) :
        '''Gets the number of people in some overlap of answers
        (e.g. males who never asked questions)'''

        overlap = self._intersect_lists(self.indices[key1][0], self.indices[key2][0])
        return len(overlap)

if __name__ == "__main__" : 
    ''' Test the class '''
    GSQ = GenderSurveyQuestions(csvfilename)
    print GSQ.gender_split()
    print GSQ.get_number_options()
    print "Never asked", GSQ.get_number('never asked')
    print "Asked", GSQ.get_number('have asked')
    print "Males who never asked", GSQ.get_number_overlap('M','never asked')
    print "Males who asked", GSQ.get_number_overlap('M','have asked')
    print "Females who never asked", GSQ.get_number_overlap('F','never asked')
    print "Females who asked", GSQ.get_number_overlap('F','have asked')
    print "\nReasons: "
    for sw in GSQ.shortwhys : 
        print sw, ': ', GSQ.get_number(sw)

    print "\n Reasons women: "
    for sw in GSQ.shortwhys : 
        print sw, ': ', GSQ.get_number_overlap('F', sw)

    print "\n Reasons men: "
    for sw in GSQ.shortwhys : 
        print sw, ': ', GSQ.get_number_overlap('M', sw)
    
