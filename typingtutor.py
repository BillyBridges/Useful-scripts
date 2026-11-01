#FOR WINDOWS
import tkinter as tk
from tkinter import simpledialog, messagebox
import os
import random
import time

# Converted from the original code in Delphi's Pascal.

# This script runs a typing tutor, mainly made for the brazilian typing system.
# Although if you have the "United States International" keyboard layout,
# you can type all the required characters and complete the course.

# The original Delphi version overrides the system's input functions and
# converts the keystrokes to either the brazilian or american keyboard layouts in
# order to show a drawing of the hands with the correct finger marked for the ex-
# pected keypress. This version doesn't implement this in order to allow the user
# to use different and custom layouts and key mappings.

# The lessons and parameters from the original Delphi code.
# I've kept the first element as a placeholder for 1-based indexing.

LESSONS = [
    'lesson out of range',
    'asdfg asdfg asdfg asdfg asdfg asdfg asdfg asdfg asdfg asdfg asdfg asdfg',#asdfg 12 vezes,
    'çlkjh çlkjh çlkjh çlkjh çlkjh çlkjh çlkjh çlkjh çlkjh çlkjh çlkjh çlkjh çlkjh',
    'asdfg hjklç asdfg hjklç asdfg hjklç asdfg hjklç asdfg hjklç asdfg hjklç',
    'fada fada fada fada fada fada fada fada fada fada fada fada fada fada',
    'hjklç hjklç hjklç hjklç hjklç hjklç hjklç hjklç hjklç hjklç hjklç hjklç hjklç',
    'çlkjh gfdsa çlkjh gfdsa çlkjh gfdsa çlkjh gfdsa çlkjh gfdsa çlkjh gfdsa',
    'gfdsa gfdsa gfdsa gfdsa gfdsa gfdsa gfdsa gfdsa gfdsa gfdsa gfdsa gfdsa',
    'kjhçl kjhçl kjhçl kjhçl kjhçl kjhçl kjhçl kjhçl kjhçl kjhçl kjhçl kjhçl kjhçl',
    'asa asa asa asa asa asa asa asa asa asa asa asa asa asa asa asa asa',
    'lkjçh lkjçh lkjçh lkjçh lkjçh lkjçh lkjçh lkjçh lkjçh lkjçh lkjçh lkjçh lkjçh',
    'faça faça faça faça faça faça faça faça faça faça faça faça faça faça',
    'afaga afaga afaga afaga afaga afaga afaga afaga afaga afaga afaga',
    'hçlkj hçlkj hçlkj hçlkj hçlkj hçlkj hçlkj hçlkj hçlkj hçlkj hçlkj hçlkj hçlkj',
    'laça laça laça laça laça laça laça laça laça laça laça laça laça laça laça',
    'safa safa safa safa safa safa safa safa safa safa safa safa safa safa safa',
    'jhçlk jhçlk jhçlk jhçlk jhçlk jhçlk jhçlk jhçlk jhçlk jhçlk jhçlk jhçlk jhçlk',
    'assa assa assa assa assa assa assa assa assa assa assa assa assa',
    'haja haja haja haja haja haja haja haja haja haja haja haja haja haja haja',
    'afaga a assa afaga a assa afaga a assa afaga a assa afaga a assa afaga',
    'falsa falsa falsa falsa falsa falsa falsa falsa falsa falsa falsa falsa falsa',
    'fala da fada fala da fada fala da fada fala da fada fala da fada fala da fada',
    'qwert qwert qwert qwert qwert qwert qwert qwert qwert qwert qwert qwert',
    'poiuy poiuy poiuy poiuy poiuy poiuy poiuy poiuy poiuy poiuy poiuy poiuy',
    'wertq wertq wertq wertq wertq wertq wertq wertq wertq wertq wertq wertq',
    'yuiop yuiop yuiop yuiop yuiop yuiop yuiop yuiop yuiop yuiop yuiop yuiop',
    'rtqwe rtqwe rtqwe rtqwe rtqwe rtqwe rtqwe rtqwe rtqwe rtqwe rtqwe rtqwe',
    'qawsedrftg qawsedrftg qawsedrftg qawsedrftg qawsedrftg qawsedrftg',
    'oiuyp oiuyp oiuyp oiuyp oiuyp oiuyp oiuyp oiuyp oiuyp oiuyp oiuyp oiuyp',
    'ertqw ertqw ertqw ertqw ertqw ertqw ertqw ertqw ertqw ertqw ertqw ertqw',
    'iuypo iuypo iuypo iuypo iuypo iuypo iuypo iuypo iuypo iuypo iuypo iuypo',
    'trewq trewq trewq trewq trewq trewq trewq trewq trewq trewq trewq trewq',
    'uypoi uypoi uypoi uypoi uypoi uypoi uypoi uypoi uypoi uypoi uypoi uypoi',
    'qwert yuiop qwert yuiop qwert yuiop qwert yuiop qwert yuiop qwert yuiop',
    'ypoiu ypoiu ypoiu ypoiu ypoiu ypoiu ypoiu ypoiu ypoiu ypoiu ypoiu ypoiu',
    'raça raça raça raça raça raça raça raça raça raça raça raça raça raça',
    'poiuy trewq poiuy trewq poiuy trewq poiuy trewq poiuy trewq poiuy trewq',
    'ter ter ter ter ter ter ter ter ter ter ter ter ter ter ter ter ter ter ter ter',
    'dedal dedal dedal dedal dedal dedal dedal dedal dedal dedal dedal dedal',
    'terra terra terra terra terra terra terra terra terra terra terra terra terra',
    'pçolikujyh pçolikujyh pçolikujyh pçolikujyh pçolikujyh pçolikujyh',
    'pipo pipo pipo pipo pipo pipo pipo pipo pipo pipo pipo pipo pipo pipo pipo',
    'apupa apupa apupa apupa apupa apupa apupa apupa apupa apupa apupa',
    'poupo poupo poupo poupo poupo poupo poupo poupo poupo poupo poupo',
    'quero quero quero quero quero quero quero quero quero quero quero quero',
    'espero espero espero espero espero espero espero espero espero espero',
    'quero quer queijo qualquer quarto queira qualidade',
    'esporo espiritual errata epiglote erguer erudito epigastrio',
    'raro rato roupa restrito restaura resulta ressurge regalo',
    'terrestre terraço trajeto tratado tratasse trilogia',
    'urdir ultraja urtiga urso usura usufruir utopia ultrajoso',
    'irregular irradiar irrefutado idade ideologia idealista',
    'oferta outorga outrora ouriço ouropel orar ourejar',
    'produto professor prolifera prossegue propulsor pulseira',
    'aforquilhado agreste atapetado atordoar alegoria',
    'sussurro sulfuroso soluço sigilo sideral serrote',
    'desgasta desforra dissoluto distrato digital dolorido',
    'flagelo fisiologia fisioterapia fraude fruir',
    'galego galope geografia gorgulho gorjeta grego grosseiro',
    'heliografia hepatite hidrosfera hipossulfato haste',
    'jaqueta jeitoso jogral julho joelho jurado jejuar',
    'jarro furo jogo quilo leiteiro lareira leopardo',
    'ladeira laçarote lagarto largura legislador ligeiro',
    'zxcvb zxcvb zxcvb zxcvb zxcvb zxcvb zxcvb zxcvb zxcvb zxcvb zxcvb',
    ';.,mn ;.,mn ;.,mn ;.,mn ;.,mn ;.,mn ;.,mn ;.,mn ;.,mn ;.,mn ;.,mn ;.,mn',
    'bvcxz bvcxz bvcxz bvcxz bvcxz bvcxz bvcxz bvcxz bvcxz bvcxz bvcxz',
    '.,mn; .,mn; .,mn; .,mn; .,mn; .,mn; .,mn; .,mn; .,mn; .,mn; .,mn; .,mn;',
    'bzxcv bzxcv bzxcv bzxcv bzxcv bzxcv bzxcv bzxcv bzxcv bzxcv bzxcv',
    ',mn;. ,mn;. ,mn;. ,mn;. ,mn;. ,mn;. ,mn;. ,mn;. ,mn;. ,mn;. ,mn;. ,mn;.',
    'zaxscdvfbg zaxscdvfbg zaxscdvfbg zaxscdvfbg zaxscdvfbg zaxscdvfbg',
    'cvbzx cvbzx cvbzx cvbzx cvbzx cvbzx cvbzx cvbzx cvbzx cvbzx cvbzx',
    'vbzxc vbzxc vbzxc vbzxc vbzxc vbzxc vbzxc vbzxc vbzxc vbzxc vbzxc',
    'qazwsxedcrfvtgb qazwsxedcrfvtgb qazwsxedcrfvtgb qazwsxedcrfvtgb',
    'nm;., nm;., nm;., nm;., nm;., nm;., nm;., nm;., nm;., nm;., nm;., nm;.,',
    'n;.,m n;.,m n;.,m n;.,m n;.,m n;.,m n;.,m n;.,m n;.,m n;.,m n;.,m n;.,m',
    ';ç.l,kmjnh ;ç.l,kmjnh ;ç.l,kmjnh ;ç.l,kmjnh ;ç.l,kmjnh ;ç.l,kmjnh',
    'zxcvb nm,.; zxcvb nm,.; zxcvb nm,.; zxcvb nm,.; zxcvb nm,.; zxcvb nm,.;',
    ';.,mn bvcxz ;.,mn bvcxz ;.,mn bvcxz ;.,mn bvcxz ;.,mn bvcxz ;.,mn bvcxz',
    'pç;ol.ik,ujmyhn pç;ol.ik,ujmyhn pç;ol.ik,ujmyhn pç;ol.ik,ujmyhn',
    'a b c d e f g h i j k l m n o p q r s t u v w y z x',
    'andarilho aforismo amplexo anteparo banqueiro baixo',
    'coincide cansaço calçado começo dantesco divino devoto decide',
    'garfo gemada gangorra gelatina habita correndo horticultura',
    'leporino lenhoso levante lapela moroso marcante mala maxixe',
    'nexo ninho numeroso ninfa nefasto operosidade oprimir ovo',
    'vexado vacila vestido valente xarope xeque xifoide xilofone',
    'zangado zebra zoologia zinco zelar zumbido zero zuzu',
    'comprando portanto lamento comendo partindo distinto',
    'pupila palpita praxe prazo pois quimono questiona qualquer',
    'recebo resposta reage restinga surpreende sequazes somamos',
    'terrestre transfigura trabalho ultima usura urgente ursa',
    'bondade contabilidade coqueiro cadeia brincadeira banheiro',
    'geografia datilografia amavel imovel folhagem mensagem altissimo',
    '12345 67890 12345 67890 12345 67890 12345 67890 12345 67890',
    '09876 54321 09876 54321 09876 54321 09876 54321 09876 54321',
    'Estados Unidos da América.',
    'ESTADOS UNIDOS DA AMÉRICA. Estados Unidos da América.',
    'Exmo. Sr. Diretor Geral da Secretaria da Cidadania do Est. do Esp. Santo.',
    'Marca Registrada CIF santos FOB Recife. Caixa Postal. Estado: Pernambuco',
    'Vitória, 25 de Janeiro. Parque D. Pedro II. 200 quilos',
    'Decreto n. 349 de 28 de abril de 1938, art. 2o && 3o',
    'jackdaws love my big sphinx of quartz',
    'the quick brown fox jumps over the lazy dog',
    'xeque pedrilha tebone sady valentia majoca worky fuga zuzidi',
    'zenith philips samsung sony kowalov joker felps bosch duque xuxa',
    '_Você não é! É? Você, não foi à feira, lingüiça. Com: Cinqüenta. Melões;',
    'int f() {_Result.StrLst[!q / 72, z &&&& a] = (@i + 8 + p^ <> -$53) ? ''16/4'' : copy(#0"r", @p * 9, i^ * %x);}',
    'abcdefghijklmnopqrstuvwxyz', #todas as letras
    '~`"''^ ~`"''^ ~`"''^ ~`"''^ ~`"''^', #todas as letras que são acentuadas
    '1234567890 1234567890 1234567890', #todos os numeros
    '!@#$%^&&*() !@#$%^&&*() !@#$%^&&*()', #todos os simbolos em cima dos numeros
    '`~!1@2#3$4%5^6&7*8(9)0_-+=', #todos os caracteres da primeira fileira
    ',<.>/?;:''"[{]}-_=+\\|', #todos os simbolos da direita
    'Abcd: Efgh? Ijkl, Mnop Qrst. Uvwxç, YzéãÀô. 12345;', #Lição essencial
    'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`~1!2@3#4$5%6^7&8*9(0)-_=+[{]};:\'",<.>/?\\| '] # todos os caracteres

# Time and error limits for each lesson
# (NSec, NErrors, NRep from Delphi code)
# Note from human: I changed the dictionary for the lesson parameters back to list again
# and inserted a phantom element at the beginning to match the original index system
NSec = [
    480,480,480,480,370,480,460,450,480,390,480,420,390,420,370,390,440,390,380,455,
    380,420,420,420,450,450,460,570,440,450,440,420,440,460,440,340,420,330,380,320
    ,430,350,450,440,450,450,325,325,325,320,325,320,320,325,320,320,320,300,330
    ,330,325,320,340,380,380,440,440,440,440,530,420,420,530,440,440,470,530,530
    ,430,350,440,440,440,440,440,440,440,440,440,450,440,440,460,380,380,350,460
    ,540,540,360,360,260,300,350,360,430,530,55,110,60,100,100,70,130,380]

NErrors = [
    6,6,6,11,5,6,10,6,6,5,6,6,5,6,6,5,6,5,6,6,6,6,6,6,6,6,6,10,6,6,6,6,6,6,6,6,6,6,6
    ,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6
    ,10,5,8,8,8,8,8,8,8,8,8,8,8,8,8,6,6,9,8,7,7,6,6,6,6,6,6,6,5,1,3,0,3,3,3,1,3]

NRep = [
    15,15,15,15,10,15,15,15,15,10,15,15,10,15,15,10,15,10,15,15,15,15,15,15,15,15,15,
    15,15,15,15,15,15,15,15,15,15,10,15,10,15,10,15,15,15,15,15,15,15,15,15,15,15,
    15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,10,
    10,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,10,17,15,15,15,15,15,15,10]
    
    
RANDOM_FLOATS_W = [random.random() for _ in range(16)]
RANDOM_FLOATS_R = [random.random() for _ in range(512)]

# Two global integer pointers, initialized to 0.
# The read_pointer tracks the next number to be read.
# The write_pointer tracks the next position to be written to.
read_pointer_r = 0
write_pointer_r = 1
read_pointer_w = 2
write_pointer_w = 3
_pointers_ = [0, 0, 0, 0]

def info_float(_v):
    

    """
    #print((((_v / 2) + 1)))
    a = _v / (int((_v / 2.1131111111111111) + 1.1311111111111111)) + (_v - int(_v))
    while a < 0.5:
        a = a * 2
    while a >= 1:
        a = a / 2
    #print(a)    
    return a * random.random()
    """
    b = _v
    a = 32
    while True:
        while b > (2**a):
            b = b / (2**a)
        a -= 1
        if (a < 1): 
            break
    if (b > 1):
        b = b / 2
    #print(b)
    return b * random.random()
    
def read_float(_list_p, _pt_):
    """
    Reads a single floating-point number from the global list
    at the current read_pointer position. The pointer is then
    incremented and circles back to 0 if it reaches the end.

    Returns:
        float: The floating-point number read from the list.
    """

    
    # Store the value at the current read_pointer.
    value = _list_p[_pointers_[_pt_]]
    
    # Increment the pointer and use the modulo operator (%)
    # to ensure it wraps around to 0 after reaching 511.
    _pointers_[_pt_] = (_pointers_[_pt_] + 1) % len(_list_p)
    
    return value

def write_float(_list_p, new_value, _pt_):
    """
    Writes a single floating-point number to the global list
    at the current write_pointer position. The pointer is then
    incremented and circles back to 0 if it reaches the end.

    Args:
        new_value (float): The floating-point number to write.
    """
 
    
    # Write the new_value to the list at the current pointer position.
    _list_p[_pointers_[_pt_]] = new_value
    
    # Increment the pointer and use the modulo operator (%)
    # to ensure it wraps around to 0 after reaching 511.
    _pointers_[_pt_] = (_pointers_[_pt_] + 1) % len(_list_p)
    
def calculate_and_truncate(phantom, mod_parameter):
    """
    Reads every float from the global list, multiplies each by a specific
    large integer, and adds the result to a running total. The final
    sum is then truncated to an integer and returned modulo the
    provided parameter.

    Args:
        mod_parameter (int): The parameter to use for the modulo operation.

    Returns:
        int: The truncated result modulo the mod_parameter.
    """
  
    local_sum = 0
    
    # The large integer to multiply by.
    # Note: 4503599627370495 is 2^52 - 1. This is a very large integer.
    # The floating point precision in a 64-bit float is 52 bits of
    # mantissa (significand), meaning it can accurately represent all
    # integers up to 2^53. Multiplying by a number close to 2^52
    # will essentially shift the decimal point to the right,
    # converting the fractional part of the random number into a large integer.
    large_integer = 4503599627370493 / 2.1111111111111111
    _ct = time.time()
    write_float(RANDOM_FLOATS_W, read_float(RANDOM_FLOATS_R,read_pointer_r),write_pointer_w)
    
    # Iterate through all the floats in the list.
    for i in range(len(RANDOM_FLOATS_W)):
        # Multiply the float by the large integer and add to the sum.
        _aux = RANDOM_FLOATS_W[i]
        local_sum = local_sum / 3
        local_sum += (_aux * large_integer)
        RANDOM_FLOATS_W[i] = info_float(((((RANDOM_FLOATS_W[i]) + (RANDOM_FLOATS_W[(i + 1) % len(RANDOM_FLOATS_W)]) + _ct)) *_aux) + _aux + (_ct));
        
    #print(local_sum)
    #print(_pointers_)
    for i in range(43):
        local_sum += random.random()
    for i in range(11):
        local_sum += random.randint(1,79)        
    
    # Return the truncated integer modulo the parameter.
    #print((int(local_sum)) % (mod_parameter + 1))
    #print(int(local_sum))
    #print((local_sum))
    return (int(local_sum)) % (mod_parameter + 1)

class TypingTutorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Typing Tutor")
        self.lesson_number = 1
        self.repetition_count = 1
        self.total_lesson_errors = 0
        self.total_lesson_time = 0.0
        self.start_time = None
        self.username = None
        self.ReqChar = ""
        self.current_lesson_string = LESSONS[0]

        # Prompt for the user's name to enable personalized progress saving.
        self.get_username()
        self.master.lift()
        self.master.focus_force()
        
        # UI elements
        self.lesson_label = tk.Label(master, text="", font=("Helvetica", 16))
        self.lesson_label.pack(pady=10)
        
        self.progress_label = tk.Label(master, text="", font=("Helvetica", 12))
        self.progress_label.pack(pady=5)
        
        self.input_entry = tk.Text(master, height=10, width=80, font=("Linux Libertine", 36), wrap="word")
        self.input_entry.pack(pady=10)
        
        # Create tags for correct, incorrect, and highlighted characters
        self.input_entry.tag_config("correct", foreground="green")
        self.input_entry.tag_config("incorrect", foreground="red")
        self.input_entry.tag_config("highlight", background="lightblue")
        
        # Bind key events to our check_input function.
        self.input_entry.bind('<Key>', self.check_input)
        
        self.current_index = 0
        self.update_ui()
        self.load_progress()
        self.start_lesson()

    def get_username(self):
        """
        Prompts the user for their name to load/save progress.
        """
        self.username = simpledialog.askstring("Username", "Please enter your name:")
        if not self.username:
            messagebox.showerror("Error", "Username is required. The application will close.")
            self.master.destroy()

    def update_ui(self):
        """
        Updates the UI elements with current lesson and progress information.
        """
        # Check if the lesson number is within the valid range before updating
        if self.lesson_number >= len(LESSONS):
            return

        self.lesson_label.config(text=f"Lesson {self.lesson_number}")
        # Display the user, current repetition, and total errors for the lesson.
        time_elapsed = time.time() - self.start_time if self.start_time else 0
        #time_elapsed = time.time() - self.total_lesson_time if self.start_time else 0
        #self.ReqChar = self.current_lesson_string[self.current_index]
        self.progress_label.config(text=f"User: {self.username}\nRepetition: {self.repetition_count}/{NRep[self.lesson_number]}\nErrors: {self.total_lesson_errors}\nTime: {int(self.total_lesson_time + time_elapsed)}s\n{self.ReqChar}")
        #self.master.after(100, self.update_ui)

    def save_progress(self):
        """
        Saves the current lesson number to a file named after the user.
        """
        filename = f"typing_tutor_progress_{self.username}.txt"
        with open(filename, "w") as f:
            f.write(str(self.lesson_number))

    def load_progress(self):
        """
        Loads the saved lesson number from a file named after the user.
        """
        filename = f"typing_tutor_progress_{self.username}.txt"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                self.lesson_number = int(f.read())

    def start_lesson(self):
        """
        Loads the current lesson string and resets state for a new repetition.
        """
        # Ensure we don't go out of bounds of the LESSONS list.
        if self.lesson_number >= len(LESSONS):
            messagebox.showinfo("Congratulations!", "You have completed all lessons!")
            self.master.destroy()
            return
            
        self.current_lesson_string = self.get_lesson_string(self.lesson_number)
        
        # Clear the memo and insert the lesson string
        self.input_entry.config(state="normal")
        self.input_entry.delete("1.0", tk.END)
        self.input_entry.insert("1.0", self.current_lesson_string)
        
        # Disable the memo initially, user input will be managed by check_input
        self.input_entry.config(state="disabled")
        
        self.current_index = 0
        self.start_time = time.time()
        self.ReqChar = self.current_lesson_string[self.current_index]
        self.update_ui()
        self.highlight_current_char()
        self.input_entry.focus_set()

    def highlight_current_char(self):
        """
        Highlights the character at the current typing position.
        """
        self.input_entry.tag_remove("highlight", "1.0", tk.END)
        if self.current_index < len(self.current_lesson_string):
            start_pos = f"1.0+{self.current_index}c"
            end_pos = f"1.0+{self.current_index + 1}c"
            self.input_entry.tag_add("highlight", start_pos, end_pos)

    def check_input(self, event):
        """
        Compares user input with the lesson string.
        Corrects misbehaviors by preventing incorrect characters from being displayed,
        and correctly counting errors.
        """
        write_float(RANDOM_FLOATS_R, info_float(time.time()), write_pointer_r)
        typed_char = event.char
        
        # Special case for Enter key at the end of the lesson string
        if event.keysym == 'Return' and self.current_index == len(self.current_lesson_string):
            self.end_lesson()
            #self.ReqChar = "Enter"
            self.update_ui() 
            return "break"
        
        # Ignore non-character keys and prevent them from being typed
        if not typed_char or event.keysym in ['BackSpace', 'Delete', 'Shift_L', 'Shift_R', 'Caps_Lock', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R']:
            self.update_ui() 
            return "break"
            
        # Only process if we're not at the end of the string
        if self.current_index < len(self.current_lesson_string):
            required_char = self.current_lesson_string[self.current_index]
            self.ReqChar = required_char
            self.update_ui()
            

            if typed_char == required_char:
                # Apply the "correct" tag to the typed character
                self.input_entry.tag_remove("highlight", "1.0", tk.END)
                self.input_entry.tag_add("correct", f"1.0+{self.current_index}c", f"1.0+{self.current_index+1}c")
                self.current_index += 1
                self.highlight_current_char()
                if self.current_index < len(self.current_lesson_string):
                    required_char = self.current_lesson_string[self.current_index]
                    self.ReqChar = required_char
                else:
                    self.ReqChar = "Enter"
            else:
                # Apply the "incorrect" tag and increment total error count for the lesson
                #self.input_entry.tag_remove("highlight", "1.0", tk.END)
                self.input_entry.tag_add("incorrect", f"1.0+{self.current_index}c", f"1.0+{self.current_index+1}c")
                self.total_lesson_errors += 1
            self.update_ui() 
            # The return "break" prevents Tkinter from automatically inserting
            # the character, giving us full control.
            return "break"
        else: 
            self.ReqChar = "Enter"
            # Apply the "incorrect" tag and increment total error count for the lesson
            self.input_entry.tag_remove("highlight", "1.0", tk.END)
            #self.input_entry.tag_add("incorrect", f"1.0+{self.current_index}c", f"1.0+{self.current_index+1}c")
            self.total_lesson_errors += 1
            self.update_ui()        
        return "break" # Also prevents any typing after the end of the string

    def end_lesson(self):
        """
        Checks if the user passed the repetition and moves on to the next.
        """
        time_taken = time.time() - self.start_time
        self.total_lesson_time += time_taken
        self.repetition_count += 1
        
        max_reps = NRep[self.lesson_number]
        
        if self.repetition_count > max_reps:
            # Check the total performance for the entire lesson.
            passed = (self.total_lesson_time <= NSec[self.lesson_number]) and \
                     (self.total_lesson_errors <= NErrors[self.lesson_number])
            
            if passed:
                messagebox.showinfo("Lesson Complete", f"You passed lesson {self.lesson_number}!")
                self.lesson_number += 1
                self.save_progress()
            else:
                messagebox.showwarning("Lesson Failed", "You did not meet the total requirements for all repetitions. Please try again.")
            
            # Reset for the next lesson.
            self.repetition_count = 1
            self.total_lesson_errors = 0
            self.total_lesson_time = 0
            self.start_lesson()
            self.update_ui() 
        else:
            # Reset for the next repetition of the same lesson.
            self.start_lesson()

    def get_lesson_string(self, lesson_num):
        """Handles getting the correct lesson string, including randomization."""
        # Use specific randomization functions for the last 8 lessons
        if lesson_num == 107:
            return self.randomize_107()
        elif lesson_num == 108:
            return self.randomize_108()
        elif lesson_num == 109:
            return self.randomize_109()
        elif lesson_num == 110:
            return self.randomize_110()
        elif lesson_num == 111:
            return self.randomize_111()
        elif lesson_num == 112:
            return self.randomize_112()
        elif lesson_num == 113:
            return self.randomize_113()
        elif lesson_num == 114:
            return self.randomize_114()
        else:
            return LESSONS[lesson_num]

    # --- New randomization functions replicating Delphi code ---

    def randomize_114(self):
        tilde = 'õãñã'
        circumflex = 'îôûâêê'
        acute = 'áéíóúà'
        grave = 'àèìòùà'
        dieresis = 'äëïöüü'

        ls = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZçÇ`~1!2@3#4$5%6^7&8*9(0)-_=+[{]};:\'",<.>/?\\| '

        
        ls += tilde + circumflex + acute + grave + dieresis
        
        st = ""
        k = len(ls)
        while k > 0:
            j = calculate_and_truncate(0, len(ls) - 1)
            st += ls[j]
            k -= 1
        
        # Insert extra '&' as per original code's bug/feature
        i = 0
        while i < len(st):
            if st[i] == '&':
                st = st[:i] + '&' + st[i:]
                i += 2
            else:
                i += 1
        return st

    def randomize_112(self):

        ls = ',<.>/?;:\'"[{]}-_=+\\|'
        st = ""
        k = len(ls)
        while k > 0:
            j = calculate_and_truncate(0, len(ls) - 1)
            st += ls[j]
            k -= 1
        return st
    
    def randomize_111(self):

        ls = '`~!1@2#3$4%5^6&7*8(9)0_-+='
        st = ""
        k = len(ls)
        while k > 0:
            j = calculate_and_truncate(0, len(ls) - 1)
            st += ls[j]
            k -= 1
        
        # Insert extra '&' as per original code's bug/feature
        i = 0
        while i < len(st):
            if st[i] == '&':
                st = st[:i] + '&' + st[i:]
                i += 2
            else:
                i += 1
        return st

    def randomize_110(self):
        ls = '!@#$%^&*()!@#$%^&*()!@#$%^&*()'

        
        st = ""
        k = len(ls)
        while k > 0:
            j = calculate_and_truncate(0, len(ls) - 1)
            st += ls[j]
            k -= 1

        # Insert spaces at specific positions
        st = st[:10] + ' ' + st[10:]
        st = st[:21] + ' ' + st[21:]

        # Insert extra '&' as per original code's bug/feature
        i = 0
        while i < len(st):
            if st[i] == '&':
                st = st[:i] + '&' + st[i:]
                i += 2
            else:
                i += 1
        return st

    def randomize_107(self):
        ls = 'abcdefghijklmnopqrstuvwxyz'
        st = ""
        k = len(ls)
        while k > 0:
            j = calculate_and_truncate(0, len(ls) - 1)
            st += ls[j]
            k -= 1
        return st

    def randomize_109(self):
        ls = '1234567890'
        st = ""
        k = len(ls) * 3
        while k > 0:
            j = calculate_and_truncate(0, len(ls) - 1)
            st += ls[j]
            k -= 1
        
        # Insert spaces at specific positions
        st = st[:10] + ' ' + st[10:]
        st = st[:21] + ' ' + st[21:]
        return st

    def pick_accented_letter(self, char):
        """Helper function to replicate the PickAcLett logic."""
        accent_map = {
            '~': ['õ', 'ã', 'ñ', 'ã'],
            '^': ['î', 'ô', 'û', 'â', 'ê', 'ê'],
            '`': ['à', 'è', 'ì', 'ò', 'ù', 'à'],
            '\'': ['á', 'é', 'í', 'ó', 'ú', 'á'],
            '"': ['ä', 'ë', 'ï', 'ö', 'ü', 'ü'],
        }
        return random.choice(accent_map.get(char, [char]))

    def randomize_108(self):
        ls = '~`"\'^~`"\'^~`"\'^~`"\'^~`"\'^'
        st = ""
        k = len(ls)
        while k > 0:
            j = calculate_and_truncate(0, len(ls) - 1)
            st += self.pick_accented_letter(ls[j])
            k -= 1
        
        # Insert spaces at specific positions
        st = st[:5] + ' ' + st[5:]
        st = st[:11] + ' ' + st[11:]
        st = st[:17] + ' ' + st[17:]
        st = st[:23] + ' ' + st[23:]
        return st

    def randomize_113(self):
        st = ''
        letters = 'abcdefghijklmnopqrstuvwxyzç~\'`^'
        numbers = '8042631957'
        sep = ':?,.,.;+'
        
        for _ in range(4):
            st += self.pick_accented_letter(random.choice(letters))
        j = calculate_and_truncate(0, len(sep) - 1)
        st += self.pick_accented_letter(sep[j]) + ' '
        sep = sep[:j] + sep[j+1:]
        
        for _ in range(4):
            st += self.pick_accented_letter(random.choice(letters))
        j = calculate_and_truncate(0, len(sep) - 1)
        st += self.pick_accented_letter(sep[j]) + ' '
        sep = sep[:j] + sep[j+1:]

        for _ in range(4):
            st += self.pick_accented_letter(random.choice(letters))
        j = calculate_and_truncate(0, len(sep) - 1)
        st += self.pick_accented_letter(sep[j]) + ' '
        sep = sep[:j] + sep[j+1:]

        for _ in range(4):
            st += self.pick_accented_letter(random.choice(letters))
        j = calculate_and_truncate(0, len(sep) - 1)
        st += self.pick_accented_letter(sep[j]) + ' '
        sep = sep[:j] + sep[j+1:]
        
        for _ in range(4):
            st += self.pick_accented_letter(random.choice(letters))
        j = calculate_and_truncate(0, len(sep) - 1)
        st += self.pick_accented_letter(sep[j]) + ' '
        sep = sep[:j] + sep[j+1:]
        
        for _ in range(5):
            st += self.pick_accented_letter(random.choice(letters))
        j = calculate_and_truncate(0, len(sep) - 1)
        st += self.pick_accented_letter(sep[j]) + ' '
        sep = sep[:j] + sep[j+1:]
        
        for _ in range(6):
            st += self.pick_accented_letter(random.choice(letters))
        j = calculate_and_truncate(0, len(sep) - 1)
        st += self.pick_accented_letter(sep[j]) + ' '
        sep = sep[:j] + sep[j+1:]

        for _ in range(5):
            st += self.pick_accented_letter(random.choice(numbers))
        j = calculate_and_truncate(0, len(sep) - 1)
        st += self.pick_accented_letter(sep[j])
        sep = sep[:j] + sep[j+1:]

        # Uppercase the first letter of each word
        st_list = list(st)
        if st_list:
            st_list[0] = st_list[0].upper()
        for i in range(1, len(st_list)):
            if st_list[i-1] == ' ':
                st_list[i] = st_list[i].upper()
        st = "".join(st_list)

        # Delete any '+' characters
        st = st.replace('+', '')
        return st            

# Main application loop
if __name__ == '__main__':
    print(time.time())
    root = tk.Tk()
    app = TypingTutorApp(root)
    root.mainloop()
