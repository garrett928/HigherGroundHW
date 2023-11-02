import numpy as np
import matplotlib.pyplot as plt

def main():
    # grab some user input
    prompt = input("string to transmit: ")
    print(f"Your prompt: {prompt}")

    # modulate
    prompt_modulated = bpsk_modulate(string_to_bits(prompt), noise_gen=True)
    # debug
    # print(f"Modulated prompt, elements 0-4: {prompt_modulated[:5]}")

    # plot the Constellation
    # this will only be visible before you hit a key to continue
    plt.plot(np.real(prompt_modulated), np.imag(prompt_modulated), '.')
    plt.grid(True)
    plt.xlabel("I")
    plt.ylabel("Q")
    plt.ylim((-1.5, 1.5))
    plt.xlim((-1.5, 1.5))
    plt.title("BPSK modulated prompt Constellation")
    plt.show(block=False)
    plt.pause(0.001)
    input("Press any key to continue....")

    # demod the IQ
    prompt_demodulated = bpsk_demodulate(prompt_modulated)
    prompt_decoded = prompt_demodulated.decode(encoding="ascii", errors="replace")
    print(f"Prompt decoded: {prompt_decoded}")

def bpsk_demodulate(iq_samples: np.ndarray) -> bytearray:

    # Convert complex numbers to bits (1 if real part > 0, else 0)
    bits = [1 if sample.real > 0 else 0 for sample in iq_samples]

    # Convert list of bits to bytes
    byte_arr = bytearray()
    for b in range(0, len(bits), 8):
        # Convert each 8 bits to a byte
        byte = bits[b:b+8]
        # python list comprehension 
        # i always forget the syntax https://www.w3schools.com/python/python_lists_comprehension.asp 
        byte_value = sum([bit << (7 - i) for i, bit in enumerate(byte)])
        byte_arr.append(byte_value)

    

    return byte_arr

def string_to_bits(input_string) -> list[int]:
    # Encode the string as a byte array using UTF-8
    byte_array = input_string.encode('utf-8')
    # Convert each byte to its binary representation and concatenate
    bits = []
    for byte in byte_array:
        # extend vs append because we are "concating" a list with a list
        bits.extend([int(bit) for bit in format(byte, '08b')])

    return bits

# could do more to encode like differential encoding
def bpsk_modulate(binary: list[int], noise_gen: bool = False, noise_power: float = 0.01) -> np.ndarray:
    """
    Take in a binary sequence and return an array of IQ smaples representing bpsk data.
    Args:
        binary: a binary sequence to modulate
        noise_en: whether or not to include some noise to the modulation
        noise_power: how much noise to include if including noise
    Returns:
        bpsk: a series of IQ samples representing the binary data
    """

    # could use list comprehension but i wanted to move on and didnt know a way
    # off the top of my head 
    bpsk = []
    for b in binary:
        if b == 0:
            # put symbol at -1
            symbol = np.exp(1j*np.pi) 
        else:
            # put symbol at 1
            symbol = np.exp(1j*0)
        bpsk.append(symbol)

    num_symbols = len(bpsk)

    # https://pysdr.org/content/digital_modulation.html#iq-plots-constellations
    # Additive white gaussian noise
        # white - equal power amoung freq. (uniform psd) autocorrelation of 1 and then 0's
        # gaussian - follows gaussian curve in time domain for the value it takes on. avg value of zero
    if noise_gen:
        n = (np.random.randn(num_symbols) + 1j*np.random.randn(num_symbols))/np.sqrt(2) # AWGN with unity power
        bpsk = bpsk + n * np.sqrt(noise_power)

    return bpsk
