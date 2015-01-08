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

    def _responses_in_nparrays(self) : 
        '''Turns all of the values in the self.responses_dict from a
        list to a numpy array.'''

        for k, v in self.responses_dict.iteritems() :
            self.responses_dict[k] = np.array(v)

    def _read_csv(self, gendercsv ) :
        '''Reads CSV file and separates into 9 rows.  Creates dictionary
        with each response as a key, and values are numpy files'''

        self.responses_dict = { field: [] for field in self.fields}

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

if __name__ == "__main__" : 
    ''' Test the class '''
    GSQ = GenderSurveyQuestions(csvfilename)
    print GSQ.gender_split()
    print GSQ.get_number_options()
    print GSQ.get_number('never asked')
    print GSQ.get_number('have asked')
