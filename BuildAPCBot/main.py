import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

sad_words = []

starter_encouragements = [
]

URL = 'https://official-joke-api.appspot.com/random_joke'


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = "**" + json_data[0]['q'] + "** \n- *" + json_data[0]['a'] + "*"
  return (quote)


#def check_valid_status_code(request):
  if request.status_code == 200:
    return request.json()

  return False


def get_joke():
  request = requests.get(URL)
  data = check_valid_status_code(request)

  return data


def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]


def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements


@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  options = starter_encouragements

  if message.content.startswith('!inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  Joke_words = ['!Joke', '!joke', '!JOKE', '!jok']
  if any(word in msg for word in Joke_words):
    joke = get_joke()

    if joke == False:
      await message.channel.send("I have ran out of jokes unfortunately...")
    else:
      await message.channel.send('**' + joke['setup'] + '!**\n' +
                                 joke['punchline'])

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))

  if msg.startswith("!help"):
    await message.channel.send(
      "`use **!inspire** for an inspirational quote\n\n"
      "use **!Build** for example builds and what you need to have a successful build\n\n"
      "use **!CPU** for an inspirational quote\n\n"
      "use **!GPU** for a rundown of what a GPU is\n\n"
      "use **!Tutorial** for some help whilst building the PC and selecting components\n\n"
      "use **!RAM** for information regarding RAM\n\n"
      "use **!SSD** for information on storage devices\n\n"
      "use **!MOBO** for information regarding motherboards\n\n"
      "use **!Shops** to find places to buy components\n\n"
      "use **!Community** to expand your knowledge and ask questions to like-minded individuals\n\n`"
    )

  Shops_words = ['!Shops', '!shops', '!SHOPS', '!shop', '!Shop', '!SHOP']
  if any(word in msg for word in Shops_words):
    await message.channel.send("`Shops include:`\n<https://www.newegg.ca/>\n"
                               "<https://www.bestbuy.ca/en-ca>\n"
                               "<https://www.canadacomputers.com/>\n"
                               "<https://www.amazon.ca/>\n"
                               "<https://www.memoryexpress.com/>")

  Community_words = ['!Comm', '!Community', '!COMMUNITY', '!community']
  if any(word in msg for word in Community_words):
    await message.channel.send(
      "`Communities include:`\n<https://www.reddit.com/r/techsupport/>\n"
      "<https://www.reddit.com/r/buildapc/>\n"
      "<https://www.reddit.com/r/buildapcsales/>\n"
      "<https://discord.com/invite/buildapc>\n")

  CPU_words = ['!CPU', '!Cpu', '!cpu', '!Central', '!central']
  if any(word in msg for word in CPU_words):
    await message.channel.send(
      "A **central processing unit** (CPU), also called a central processor, main processor or just processor, is the electronic circuitry that executes instructions comprising a computer program. The CPU performs basic arithmetic, logic, controlling, and input/output (I/O) operations specified by the instructions in the program. This contrasts with external components such as main memory and I/O circuitry,[1] and specialised processors such as graphics processing units (GPUs). The form, design, and implementation of CPUs have changed over time, but their fundamental operation remains almost unchanged. Principal components of a CPU include the arithmetic–logic unit (ALU) that performs arithmetic and logic operations, processor registers that supply operands to the ALU and store the results of ALU operations, and a control unit that orchestrates the fetching (from memory), decoding and execution (of instructions) by directing the coordinated operations of the ALU, registers and other components. \n\n`Examples including:\n- Intel i7-4790k \n- Ryzen 5 3600x`"
    )
  Cody_words = ['Cody','CODY','cody']
  if any(word in msg for word in Cody_words):
    await message.channel.send("hahahahahah CODY IS STUPID LOL")
  Bench_words = ['!Benchmark', '!benchmark', '!BENCHMARK', '!Bench']
  if any(word in msg for word in Bench_words):
    await message.channel.send(
      "`In order to benchmark your PC components yourself it is reccommended to use:`\n\n**GPU:**\nHeaven's Benchmark - \n<https://benchmark.unigine.com/heaven>\n\n**CPU:** \nIt is reccommended to read this article prior to any attempt at benchmarking a CPU \n<https://www.comparitech.com/net-admin/how-to-cpu-benchmark-test/> \n\nFor general information regarding either it is reccommended to use:\n <https://www.userbenchmark.com/>"
    )

  Tutorial_words = [
    '!Tutorial', '!tutorial', '!TUTORIAL', '!Guide', '!GUIDE', '!guide'
  ]
  if any(word in msg for word in Tutorial_words):
    await message.channel.send(
      "`Highly Reccomended Video Tutorials:`\n\n**Building the physical PC:** <https://youtu.be/PXaLc9AYIcg>\n\n**Deciding on components:** <https://youtu.be/j_DcWgxMZ3k>\n\n**PC builder:** <https://pcpartpicker.com/>"
    )

  GPU_words = ['!GPU', '!gpu', '!Gpu', '!Graphics', '!graphics', '!GRAPHICS']
  if any(word in msg for word in GPU_words):
    await message.channel.send(
      "**The graphics processing unit, or GPU**, has become one of the most important types of computing technology, both for personal and business computing. Designed for parallel processing, the GPU is used in a wide range of applications, including graphics and video rendering. Although they’re best known for their capabilities in gaming, GPUs are becoming more popular for use in creative production and artificial intelligence (AI).\nGPUs were originally designed to accelerate the rendering of 3D graphics. Over time, they became more flexible and programmable, enhancing their capabilities. This allowed graphics programmers to create more interesting visual effects and realistic scenes with advanced lighting and shadowing techniques. Other developers also began to tap the power of GPUs to dramatically accelerate additional workloads in high performance computing (HPC), deep learning, and more.\n\n`Examples including:\n- 980ti\n- 3060ti\n- Radeon 6700XT`"
    )

  RAM_words = ['!RAM', '!Ram', '!ram', '!RandomAccesMemory', '!Random']
  if any(word in msg for word in RAM_words):
    await message.channel.send(
      "**RAM stands for random access memory**, and it’s one of the most fundamental elements of computing. RAM is a temporary memory bank where your computer stores data it needs to retrieve quickly. RAM keeps data easily accessible so your processor can quickly find it without having to go into long-term storage to complete immediate processing tasks.\nRAM is divided into storage, speed, and type \n\nfor example: \n**16 gb of 3600MHz DDR4 RAM** | *DDR4 means Double Data Rate version 4, it is an attestment to how new the RAM's technology is*"
    )

  PCRequirements_words = ['!Build', '!build', '!BUILD']
  if any(word in msg for word in PCRequirements_words):
    await message.channel.send(
      "`PC Requirements:\n- PC Case\n- CPU\n- GPU\n- RAM\n- Motherboard\n- Power Supply \n- SSD/HDD (Solid State Drive)/(Hard Drive)\n- OS (Windows, Linux, etc.)\n- Monitor \n- Keyboard \n- Mouse`\n\nHigh end Build example:\n <https://ca.pcpartpicker.com/list/QytDNc>\n\nMid end Build example: \n<https://ca.pcpartpicker.com/list/8JQHDq>"
    )

  SSD_words = ['!Ssd', '!SSD', '!ssd']
  if any(word in msg for word in SSD_words):
    await message.channel.send(
      "In terms of storage, a hard drive is not reccomended whilst an SSD is. **Solid-state drives (SSDs)** are the most common storage drives today. SSDs are smaller and faster than hard disk drives (HDDs). SSDs are noiseless and allow PCs to be thinner and more lightweight. Hard disk drives (HDDs) are more common in older devices."
    )

  Mobo_words = [
    '!mobo', '!MOBO', '!Mobo', '!Motherboard', '!MOTHERBOARD', '!motherboard'
  ]
  if any(word in msg for word in Mobo_words):
    await message.channel.send(
      "A **motherboard** (also called mainboard, main circuit board,[1] mb, mboard, backplane board, base board, system board, logic board or mobo) is the main printed circuit board (PCB) in general-purpose computers and other expandable systems. It holds and allows communication between many of the crucial electronic components of a system, such as the central processing unit (CPU) and memory, and provides connectors for other peripherals. Unlike a backplane, a motherboard usually contains significant sub-systems, such as the central processor, the chipset's input/output and memory controllers, interface connectors, and other components integrated for general use.\n\n`Examples include: \n- Gigabyte Z690 Aorus Pro \n- ASRock Z690 Taichi`"
    )


  PSU_words = [
    '!Psu', '!PSU', '!psu', '!PowerSupply', '!powersupply', '!POWERSUPPLY'
  ]
  if any(word in msg for word in PSU_words):
    await message.channel.send(
      "**Power Supply Units (PSU)** do not supply systems with power - instead they convert it. Specifically, a power supply converts the alternating high voltage current (AC) into direct current (DC), and they also regulate the DC output voltage to the fine tolerances required for modern computing components. It is reccomended to select a power supply with gold+ rating and go well above the actual wattage of your PC ranging from (150W-double the wattage of your PC) <https://www.newegg.ca/tools/power-supply-calculator/> \n\n`Examples include:\n- Corsair RM650 650 W 80+ Gold Certified \n- Corsair HX1200 Platinum`"
    )


keep_alive()
client.run(os.getenv('TOKEN'))
