import bcrypt
from nltk.corpus import words
import time
from multiprocessing import Pool, cpu_count

HASHES = {
    'Bilbo': '$2b$08$J9FW66ZdPI2nrIMcOxFYI.qx268uZn.ajhymLP/YHaAsfBGP3Fnmq',
    'Gandalf': '$2b$08$J9FW66ZdPI2nrIMcOxFYI.q2PW6mqALUl2/uFvV9OFNPmHGNPa6YC',
    'Thorin': '$2b$08$J9FW66ZdPI2nrIMcOxFYI.6B7jUcPdnqJz4tIUwKBu8lNMs5NdT9q',
    'Fili': '$2b$09$M9xNRFBDn0pUkPKIVCSBzuwNDDNTMWlvn7lezPr8IwVUsJbys3YZm',
    'Kili': '$2b$09$M9xNRFBDn0pUkPKIVCSBzuPD2bsU1q8yZPlgSdQXIBILSMCbdE4Im',
    'Balin': '$2b$10$xGKjb94iwmlth954hEaw3O3YmtDO/mEFLIO0a0xLK1vL79LA73Gom',
    'Dwalin': '$2b$10$xGKjb94iwmlth954hEaw3OFxNMF64erUqDNj6TMMKVDcsETsKK5be',
    'Oin': '$2b$10$xGKjb94iwmlth954hEaw3OcXR2H2PRHCgo98mjS11UIrVZLKxyABK',
    'Gloin': '$2b$11$/8UByex2ktrWATZOBLZ0DuAXTQl4mWX1hfSjliCvFfGH7w1tX5/3q',
    'Dori': '$2b$11$/8UByex2ktrWATZOBLZ0Dub5AmZeqtn7kv/3NCWBrDaRCFahGYyiq',
    'Nori': '$2b$11$/8UByex2ktrWATZOBLZ0DuER3Ee1GdP6f30TVIXoEhvhQDwghaU12',
    'Ori': '$2b$12$rMeWZtAVcGHLEiDNeKCz8OiERmh0dh8AiNcf7ON3O3P0GWTABKh0O',
    'Bifur': '$2b$12$rMeWZtAVcGHLEiDNeKCz8OMoFL0k33O8Lcq33f6AznAZ/cL1LAOyK',
    'Bofur': '$2b$12$rMeWZtAVcGHLEiDNeKCz8Ose2KNe821.l2h5eLffzWoP01DlQb72O',
    'Durin': '$2b$13$6ypcazOOkUT/a7EwMuIjH.qbdqmHPDAC9B5c37RT9gEw18BX6FOay'
}

def get_word_list():
    potential_words = words.words()
    final_words = []
    for word in potential_words:
        if len(word) >= 6 and len(word) <= 10:
            final_words.append(word)
    return final_words

def check_password(args):
    word, hash_value = args
    if bcrypt.checkpw(word.encode('utf-8'), hash_value.encode('utf-8')):
        return word
    return None

def crack_hash(user, hash_value, wordlist):
    start = time.time()
    print(f"Cracking hash for {user}: {hash_value}")
    
    args_list = [(word, hash_value) for word in wordlist]
    
    num_processes = cpu_count() - 1
    print(f"num_processes: {num_processes} \n")
    with Pool(processes=num_processes) as pool:
        results = pool.imap_unordered(check_password, args_list, chunksize=100)
        
        for result in results:
            if result is not None:
                end = time.time()
                total = end - start
                print(f"Found password for {user}: {result} in {total:.2f} seconds")
                pool.terminate() 
                return (user, hash_value, result, total)
    
    print(f"Password not found for {user}")
    return None

def check_hashes():
    answers = []
    wordlist = get_word_list()
    
    for user, hash_value in HASHES.items():
        result = crack_hash(user, hash_value, wordlist)
        if result:
            answers.append(result)

    return answers

if __name__ == '__main__':
    print(check_hashes())