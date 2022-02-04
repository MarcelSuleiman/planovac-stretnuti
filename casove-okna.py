#
#   povedzme, ze mame dvoch ludi, ktori maju vo svojom kalendari 2 udaje
#   jeden hovori o tom, od kedy do kedy maju schodzky
#   druhy od kedy do kedy maju aktivnu cast dna
#

# osoba 1
cal001 = [['9:00', '10:30'], ['12:00', '13:00'], ['16:00', '18:00']]
p1_a = ['09:00', '20:00']

# osoba 2
cal002 = [['10:00', '11:30'], ['12:30', '14:30'], ['14:30', '15:00'], ['16:00', '17:00']]
p2_a = ['10:00', '18:00']

meet_duration = 30

#
#   mozeme predpokladat ze udaje v cal001, cal002 su uz zotriedene -> txt vystup
#   treba najst take casove okna, kedy sa tieto dve osoby mozu stretnut a v akych casoch
#   by si mohli naplanovat spolocne online stretnutie v dlzke aspon 30 minut
#

#
# ocakavany vystup napr: [['11:30', '12:00'], ['15:00', '16:00'], ['18:00', '19:00']]
#



def create_empty_tf() -> list:
    '''
    vytvorenie listu s prazdnymi stringmi
    kde kazdy alement reprezentuje 1 minutu
    z dna
    '''
    time_frame = []
    for i in range(1440):
        time_frame.append('')
        
    return time_frame

def make_possible_time_window(possible_meetings_temp:list) -> list:
    '''
    funkcia extrahuje zaciatocnu a konecnu hodnotu (min) spolocneho volneho casoveho okna
    '''
    meeting_window_temp = []
    meeting_window = []

    meeting_window_temp.append(possible_meetings_temp[0])

    for i in range(len(possible_meetings_temp)):
        if meeting_window_temp == []:
            meeting_window_temp.append(possible_meetings_temp[i])


        if i+1 < len(possible_meetings_temp):

            if possible_meetings_temp[i] + 1 == possible_meetings_temp[i+1]:
                pass

            else:
                meeting_window_temp.append(possible_meetings_temp[i])
                meeting_window.append(meeting_window_temp)
                meeting_window_temp = []
        else:
            meeting_window_temp.append(possible_meetings_temp[len(possible_meetings_temp)-1])
            meeting_window.append(meeting_window_temp)

    #print('--->', meeting_window)
    return meeting_window

def fill_imposible_time_frames(person_window:list, time_frame:list) -> list:
    '''
    funkcia vyplni 'y' tie minuty z dna ktore uz ma dana osoba
    rezervovane pre ine stretnutie
    '''
    result = convert_time_frame(person_window)
    #print(result)

    for element in result:
        start, end = element[0], element[1]

        for i in range(start, end):
            time_frame[i] = 'y'

    return time_frame

def convert_time_frame(time_frame: list) -> int:
    '''
    funkcia prijma ako parameter list a konvertuje txt / string casovy udaj
    na jednotlive minuty v time frame.
    9:00 -> 9h, 00min od polnoci ubehlo 9*60 min + 00 min -> 9:00 == 540 min
    '''
    result = []
    result_temp = []

    def ctf(time_frame_2):
        #1D array
        temp = time_frame_2[0].split(':')
        begin_hours = int(temp[0])
        begin_minutes = int(temp[1])

        temp = time_frame_2[1].split(':')
        end_hours = int(temp[0])
        end_minutes = int(temp[1])

        start = begin_hours * 60 + begin_minutes
        end = end_hours * 60 + end_minutes

        return start, end
    
    if type(time_frame[0]) == str:
        #1D array
        start, end = ctf(time_frame)
        return start, end

    elif type(time_frame[0]) == list:
        #2D array
        for element in time_frame:

            start, end = ctf(element)

            result_temp.append(start)
            result_temp.append(end)
            result.append(result_temp)

            result_temp = []
            
        return result

def fill_impossible_time(person_window: list, time_frame: list) -> list:
    '''
    funkcia vyplni 'x' tie minuty ktore su mimo rozsah aktivnej casti dna danej osoby
    '''
    start, end = convert_time_frame(person_window)

    for i in range(start):
        time_frame[i] = 'x'

    for i in range(end, 1440):
        time_frame[i] = 'x'

    return time_frame
    #print(time_frame)

time_frame = create_empty_tf()
fill_impossible_time(p1_a, time_frame)
time_frame_p1 = fill_imposible_time_frames(cal001, time_frame)

time_frame = create_empty_tf()
fill_impossible_time(p2_a, time_frame)
time_frame_p2 = fill_imposible_time_frames(cal002, time_frame)

'''
V tejto casti kodu spojim / prekryjem casove okna jednej aj druhej osoby
tie "okienka" ktore su ostanu volne su ich spolocny volny cas
'''

for i in range(len(time_frame_p2)):
    if time_frame_p2[i] != '':
        time_frame_p1[i] = time_frame_p2[i]

possible_meetings_temp = []

for i in range(1440):
    if time_frame_p1[i] == '':
        possible_meetings_temp.append(i)

#print(possible_meetings_temp)

meeting_windows = make_possible_time_window(possible_meetings_temp)

'''
finalny vypocet a konvert jednotlivych casovych okien kedy si dane dve osoby vedia naplanovat stretnutie
'''
w = []
for element in meeting_windows:
    w_t = []

    t1_h, t1_m = element[0] // 60, element[0] % 60
    if t1_m == 0:
        t1_m = '00'

    t1_h = str(t1_h)
    t1_m = str(t1_m)

    start_time = t1_h+':'+t1_m
    w_t.append(start_time)
    
    t2_h, t2_m = (element[1]+1) // 60, (element[1]+1) % 60
    if t2_m == 0:
        t2_m = '00'
    t2_h = str(t2_h)
    t2_m = str(t2_m)

    end_time = t2_h+':'+t2_m
    w_t.append(end_time)

    w.append(w_t)

#finalny vystup
print(w)
