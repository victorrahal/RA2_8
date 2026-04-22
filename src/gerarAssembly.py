# Aluno 3: Lucas Balint Vilar
import parseExpressao
import lerArquivo

def ValidarNomeMemoria(token):
    try:
        if token.isalpha() and token.isupper() and token != 'RES':
            return True
    except ValueError:
        return 'Nome de memória invalido'


def ValidarNumero(token):
    try:
        float(token)  
        return True   # se True é numero
    except ValueError:
        return False  # se der erro, não é número


def gerarAssembly(todosTokens, arquivoSaida='ultima_exec_Assembly.s'):
    assembly = []  # lista que armazena as instruções assembly

    contadorPot = [0] # contador para gerar labels únicos de pontenciação

    # pegar as memórias usadas nos tokens
    memorias = []
    for tokens in todosTokens:
        for token in tokens:
            if ValidarNomeMemoria(token) and token not in memorias:
                memorias.append(token)

    # validar valores únicos para não dar conflito na compilação do assembly
    valores = [] # lista que armazena valores únicos
    for tokens in todosTokens:
        for token in tokens:
            if ValidarNumero(token):
                val = float(token)
                existente = False # variavel para verificar se o valor ja existe
                for v in valores:
                    if v == val: # faz a verificação
                        existente = True
                        break # se existir sai do loop
                if not existente:
                    valores.append(val) # se nao existe adiciona na lista de valores unicos

    # garantindo o numero 1 para que a potencição possa sempre ocorrer
    existente = False
    for v in valores:
        if v == 1.0:
            existente = True
            break
    if not existente:
        valores.append(1.0)

    # cabeçalho seção data para definição dos valores doubles
    assembly.append(".global _start")
    assembly.append(".data")
    assembly.append(".align 3")
    for val in valores:
        x = f"val_{str(val).replace('.', '_')}" # cria a label do valor
        assembly.append(f"{x}: .double {val}")

    # declarar memorias com valor padrão de 0.0
    for memo in memorias:
        assembly.append(f"memo_{memo}: .double 0.0")

    # guardar o resultado de cada operação
    for k in range(len(todosTokens)):
        assembly.append(f"resultado_{k}: .double 0.0")

    # cabeçalho padrão
    assembly.append(".text")
    assembly.append(".arm")
    assembly.append(".fpu vfpv3")
    assembly.append(".align 2")        
    assembly.append("_start:")

    for numLinha, tokens in enumerate(todosTokens):# percorre cada expressão
        pilhaReg = []  # pilha que armazena registradores em uso
        regsLivres = []
        for k in range(8):
            regsLivres.append(f"D{k}") 

        proximoRES = None # guarda N quando o token for um numero
                 
        for k, token in enumerate(tokens): # percorre cada token da expressão
            if token in ['(', ')']:
                continue  # ignora parênteses

            if token == 'RES':
               if proximoRES is None: # tratando o token RES
                   assembly.append(f"UDF #1") # operando sem N
                   continue
               
               N = int(float(proximoRES))
               linhaResult = numLinha - N
               
               if linhaResult < 0 or linhaResult >= numLinha:
                   assembly.append(f"UDF #2") # linha inexistente
               else:
                   if pilhaReg:
                       regTemp = pilhaReg.pop()
                       regsLivres.insert(0, regTemp)
                   reg = regsLivres.pop(0)

                   assembly.append(f"LDR R0, =resultado_{linhaResult}") # endereço do resultado da linha
                   assembly.append(f"VLDR.F64 {reg}, [R0]") # carrega o resultado no registrador
                   pilhaReg.append(reg)
                
               proximoRES = None
               continue

            if ValidarNumero (token) and k + 1 < len(tokens) and tokens[k + 1] == 'RES':
                proximoRES = token
            else:
                proximoRES = None

            if ValidarNomeMemoria(token):
                if pilhaReg:
                    r1 = pilhaReg[-1]  # peek, não pop — mantém resultado na pilha
                    assembly.append(f"LDR R0, =memo_{token}")
                    assembly.append(f"VSTR.F64 {r1}, [R0]")
                else:
                    regist = regsLivres.pop(0)
                    assembly.append(f"LDR R0, =memo_{token}")
                    assembly.append(f"VLDR.F64 {regist}, [R0]")
                    pilhaReg.append(regist)
                continue

            if ValidarNumero(token):
                reg = regsLivres.pop(0) # pega o primeiro registrador livre
                val = float(token)
                x = f"val_{str(val).replace('.', '_')}"
                assembly.append(f"LDR R0, ={x}") # carrega o endereço de x em R0
                assembly.append(f"VLDR.F64 {reg}, [R0]") # carrega o valor no registrador
                pilhaReg.append(reg)  # empilha o registrador para uso futuro

            elif token in ['+', '-', '*', '/', '//', '%', '^']:
                # desempilha os dois últimos operandos
                r2 = pilhaReg.pop()  # segundo operando
                r1 = pilhaReg.pop()  # primeiro operando
                # realiza a operação usando r1 como registrador de resultado
                match token:
                    case '+':
                        assembly.append(f"VADD.F64 {r1}, {r1}, {r2}") # operacao de soma
                    case '-':
                        assembly.append(f"VSUB.F64 {r1}, {r1}, {r2}") # oepracao de subtração
                    case '*':
                        assembly.append(f"VMUL.F64 {r1}, {r1}, {r2}") # operacao de multiplicação
                    case '/':
                        assembly.append(f"VDIV.F64 {r1}, {r1}, {r2}") # operação de divisão não inteira
                    case '//':
                        assembly.append(f"VDIV.F64 {r1}, {r1}, {r2}") # divisão não inteira
                        assembly.append(f"VCVT.S32.F64 S0, {r1}") # converte para inteiro, truncando o float
                        assembly.append(f"VCVT.F64.S32 {r1}, S0") # volta o resultado para double
                    case '%': # resto: A - (A/B) * B
                        assembly.append(f"VDIV.F64 D6, {r1}, {r2}") # divisão não inteira
                        assembly.append(f"VCVT.S32.F64 S0, D6") # converte para inteiro, truncando o float
                        assembly.append(f"VCVT.F64.S32 D6, S0") # volta o resultado para double
                        assembly.append(f"VMUL.F64 D6, D6, {r2}") # (A/B) * B
                        assembly.append(f"VSUB.F64 {r1}, {r1}, D6") # A - (A/B) * B
                    case '^': #potenciacao
                        loopPot = f"pot_{contadorPot[0]}" # label do loop da potenciacao
                        fimLoop = f"potFim_{contadorPot[0]}" # label de saida do loop da potenciacao
                        contadorPot[0] += 1 # incrementa o contador
                        assembly.append(f"VMOV.F64 D6, {r1}") # numero base
                        assembly.append(f"VMOV.F64 D7, {r2}") # numero expoente
                        assembly.append(f"LDR R0, =val_1_0") # Carrega o 1.0 no registrador
                        assembly.append(f"VLDR.F64 D5, [R0]") #D5 = 1.0
                        assembly.append(f"{loopPot}:")
                        assembly.append(f"VCVT.S32.F64 S0, D7") # converte o expoente para numero inteiro
                        assembly.append(f"VMOV R2, S0") # move o valor para um registrador geral R2
                        assembly.append(f"CMP R2, #1") # compara o expoente com o numero 1
                        assembly.append(f"BLE {fimLoop}") # sai do loop se o expoente for menor que 1
                        assembly.append(f"VMUL.F64 D6, D6, {r1}") # multiplica o numero por ele mesmo
                        assembly.append(f"VSUB.F64 D7, D7, D5") # diminui o expoente em 1 
                        assembly.append(f"B {loopPot}") # volta pro loop e reinicia o processo
                        assembly.append(f"{fimLoop}:") 
                        assembly.append(f"VMOV.F64 {r1}, D6") # move o resultado final para r1

                pilhaReg.append(r1) # resultado volta para a pilha
                regsLivres.append(r2) #libera o registrador

        # salvar o resultado no topo da pilha de resultados ao final de cada linha
        if pilhaReg:
            topo = pilhaReg[-1]
            assembly.append(f"LDR R0, =resultado_{numLinha}") # endereço da linha
            assembly.append(f"VSTR.F64 {topo}, [R0]") # salva o resultado

    # finaliza o programa para não ficar em loop
    assembly.append("    MOV R7, #1")
    assembly.append("    SWI #0")
                
    # escreve o código assembly no arquivo de saída
    with open(arquivoSaida, 'w') as f:
        for linha in assembly:
            f.write(linha + '\n')

    return assembly  # retorna a lista