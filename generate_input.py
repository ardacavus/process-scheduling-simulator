import random

def create_random_file(filename, num_processes):
    with open(filename, 'w') as f:
        for i in range(1, num_processes + 1):
            pid = f"P{i}"
            arrival = random.randint(0, 20) # 0 ile 20 arası rastgele geliş
            burst = random.randint(1, 10)   # 1 ile 10 arası iş süresi
            priority = random.randint(1, 5) # 1 ile 5 arası öncelik
            f.write(f"{pid}, {arrival}, {burst}, {priority}\n")
    print(f"'{filename}' oluşturuldu. {num_processes} adet rastgele süreç içeriyor.")

# 10 süreçli bir test dosyası oluştur
create_random_file("random_test.txt", 10)

# 100 süreçli stres testi dosyası oluştur
create_random_file("stress_test.txt", 100)