import matplotlib.pyplot as plt


def plot_aes_performance():
    block_sizes_bytes = [16, 64, 256, 1024, 8192, 16384]
    block_sizes_mb = [size / (1024 * 1024) for size in block_sizes_bytes]
    
    aes_128_mbs = [841673.24 / 1024, 2052068.44 / 1024, 2268067.27 / 1024, 2353215.15 / 1024, 2350828.20 / 1024, 2347339.52 / 1024]
    aes_192_mbs = [1341937.55 / 1024, 1645167.28 / 1024, 1949597.10 / 1024, 2002479.45 / 1024, 1928217.51 / 1024, 1938760.50 / 1024]
    aes_256_mbs = [1207987.21 / 1024, 1511039.55 / 1024, 1624147.56 / 1024, 1691938.82 / 1024, 1618636.80 / 1024, 1636956.65 / 1024]
    
    plt.figure(figsize=(12, 8))
    
    plt.plot(block_sizes_mb, aes_128_mbs, 'o-', label='AES-128')
    plt.plot(block_sizes_mb, aes_192_mbs, 's-', label='AES-192')
    plt.plot(block_sizes_mb, aes_256_mbs, '^-', label='AES-256')
    
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Block Size (MB)', fontsize=12)
    plt.ylabel('Throughput (MB/s)', fontsize=12)
    plt.title('AES: Block Size vs Throughput', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('aes_performance.png', bbox_inches='tight')
    plt.show()

def plot_rsa_performance():
    key_sizes = [512, 1024, 2048, 3072]
    
    signing_ops = [688314 / 9.98, 145140 / 9.95, 23320 / 9.97, 7883 / 9.88]
    verification_ops = [7566194 / 9.90, 2929304 / 9.91, 893527 / 9.95, 421517 / 9.93]
    
    plt.figure(figsize=(12, 8))
    
    plt.plot(key_sizes, signing_ops, 'o-', label='Signing')
    plt.plot(key_sizes, verification_ops, 's-', label='Verification')
    
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Key Size (bits)')
    plt.ylabel('Operations per Second')
    plt.title('RSA Performance: Key Size vs Throughput')
    plt.legend()
    plt.savefig('rsa_performance.png')
    plt.show()


def main():
    plot_aes_performance()
    plot_rsa_performance()

if __name__ == "__main__":
    main()
