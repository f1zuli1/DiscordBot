import aiohttp  # Eşzamansız HTTP istekleri için bir kütüphane
import random
import asyncio
from datetime import datetime,timedelta
class Pokemon:
    pokemons = {}
    # Nesne başlatma (kurucu)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.weight=None
        self.height=None
        self.hp=random.randint(70,100)
        self.power=random.randint(30,60)
        self.last_feed_time=datetime.now()
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def get_name(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve çözümlenmesi
                    return data['forms'][0]['name']  #  Pokémon adını döndürme
                else:
                    return "Pikachu"  # İstek başarısız olursa varsayılan adı döndürür


    async def load_data(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve çözümlenmesi
                    self.height=data["height"]
                    self.weight=data["weight"] 
                else:
                    return None  # İstek başarısız olursa varsayılan adı döndürür









    async def info(self):
        # Pokémon hakkında bilgi döndüren bir metot
        if not self.name:
            await self.load_data()
            self.name = await self.get_name()  # Henüz yüklenmemişse bir adın geri alınması
        return f"Pokémonunuzun ismi: {self.name}\nPokemonun boyu: {self.height/10} metre\nPokemonun kilosu: {self.weight/10} kilogram\nPokemonun sağlığı: {self.hp}\nPokemonun gücü: {self.power}"  # Pokémon adını içeren dizeyi döndürür

    async def show_img(self):
        # PokeAPI aracılığıyla bir pokémon görüntüsünün URL'sini almak için asenktron metot
                # PokeAPI aracılığıyla bir pokémonun adını almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve çözümlenmesi
                    return data["sprites"]["front_default"]  #  Pokémon adını döndürme
                else:
                    return None # İstek başarısız olursa varsayılan adı döndürür
    async def attack(self,enemy):
        if isinstance(enemy,Wizard):
            chance=random.randint(1,3)
            if chance==1:
                return "Sihirbaz kalkan kullandı..."
            
        if enemy.hp>self.power:
            enemy.hp-=self.power
            return f"@{self.pokemon_trainer} @{enemy.pokemon_trainer}'a saldırdı...\nŞuanda düşman sağlığı: {enemy.hp}"
        else:
            enemy.hp=0
            return f"@{self.pokemon_trainer} @{enemy.pokemon_trainer}'ı yendi..."
        


    async def feed(self, feed_interval= 20, hp_increase=10 ):
        current_time = datetime.now()
        delta_time = timedelta(seconds=feed_interval)  
        if (current_time - self.last_feed_time) > delta_time :
            self.hp += hp_increase
            self.last_feed_time = current_time 
            return f"Pokémon sağlığı geri yüklenir. Mevcut HP: {self.hp}"
        else:
            return f"Pokémonunuzu şu zaman besleyebilirsiniz:{self.last_feed_time+ delta_time }"





class Wizard(Pokemon):
    async def attack(self,enemy):
        magic_power=random.randint(5,14)
        self.power+=magic_power
        result= await super().attack(enemy)
        self.power-=magic_power

        return result + f"\n Sihirbaz büyülü bir saldırı yaptı eksra büyü gücü:{magic_power}"
    async def feed(self):
        return await super().feed(hp_increase=5)




class Fighter(Pokemon):
    async def attack(self,enemy):
        super_power=random.randint(3,19)
        self.power+=super_power
        result= await super().attack(enemy)
        self.power-=super_power

        return result + f"\n Sihirbaz büyülü bir saldırı yaptı eksra büyü gücü:{super_power}"
    
    async def feed(self):
        return await super().feed(feed_interval=35)






async def main():
    wizard = Wizard("ali")
    fighter = Fighter("veli")

    print(await wizard.info())
    print()
    print(await fighter.info())
    print()
    print(await fighter.attack(wizard))

if __name__ == '__main__':
    asyncio.run(main())