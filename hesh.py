import string , random


def generator() :
  dictionary = list(string.ascii_uppercase + string.ascii_lowercase + string.digits)
  print(''.join(random.sample(dictionary, 10)))

def hash_string(text: string):
    return random.getrandbits(text.digit())



if __name__ == "__main__":
    # Задание 1
    print("Задание 1")
    generator()

    # Задание 2
    print("Задание 2")
    initial_text = 'Мороз и солнце, день чудесный'.split()
    keys = ['S', 'k', '7', 9, 'm']
    for a in zip(keys, initial_text):
        print(a)