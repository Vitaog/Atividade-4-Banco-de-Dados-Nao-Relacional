from connect_database import conectar_cassandra
from produto import criar_produto, deletar_produto, editar_produto, listar_produtos


key = 0
sub = 0

session = conectar_cassandra()

while (key != 'S' and key != 's'):
    print("|---------------------Bem Vindo---------------------------------|")
    print("1-CRUD Usuário")
    print("2-CRUD Vendedor")
    print("3-CRUD Produto")
    print("|---------------------------------------------------------------|")
    key = input("Digite a opção desejada? (S para sair) ")
    print ("")

    if (key == '1'):
        print("|-------------------Menu do Usuário-----------------------------|")
        print("1-Create Usuário")
        print("2-Read Usuário")
        print("3-Update Usuário")
        print("4-Delete Usuário")
        print("|--------------------Funcionalidades----------------------------|")
        print("5-Adicionar Favoritos")
        print("6-Remover Favoritos")
        print("7-Adicionar Compra")
        print("8-Cancelar Compra")
        print("|---------------------------------------------------------------|")
        sub = input("Digite a opção desejada? (V para voltar) ")
        print ("")

        if (sub == '1'):
            print("|-------------------Criação de Usuário------------------------|")
            print ("")
            
        elif (sub == '2'):
            print("|----------------Listagem de Usuário-------------------------|")
            print ("")
        
        elif (sub == '3'):
            print("|--------------------------------------------------------------|")
            print ("")

        elif (sub == '4'):
            print("|--------------------------------------------------------------|")
            print ("")
        
        elif (sub == '5'):
            print("|--------------------------------------------------------------|")
            print ("")
        
        elif (sub == '6'):
            print("|--------------------------------------------------------------|")
            print ("")

        elif (sub == '7'):
            print("|--------------------------------------------------------------|")
            print ("")
        
        elif (sub == '8'):
            print("|--------------------------------------------------------------|")
            print ("")

            
    elif (key == '2'):
         print("|-------------------Menu do Vendedor----------------------------|")
         print("1-Create Vendedor")
         print("2-Read Vendedor")
         print("3-Update Vendedor")
         print("4-Delete Vendedor")
         print("|--------------------Funcionalidades----------------------------|")
         print("5-Adicionar Produto")
         print("6-Atualizar Produto")
         print("7-Remover Produto")
         print("|---------------------------------------------------------------|")
         sub = input("Digite a opção desejada? (V para voltar) ")
         print ("") 

         if (sub == '1'):
             print("|-------------------Criação de Vendedor------------------------|")
             print ("")
        
         elif (sub == '2'):
             print("|----------------Listagem de Vendedor-------------------------|")
             print ("")

         elif (sub == '3'):
             print("|--------------------------------------------------------------|")
             print ("")   

         elif (sub == '4'):
             print("|--------------------------------------------------------------|")
             print ("")
            
         elif (sub == '5'):
             print("|--------------------------------------------------------------|")
             print ("")
        
         elif (sub == '6'):
             print("|--------------------------------------------------------------|")
             print ("")
        
         elif (sub == '7'):
             print("|--------------------------------------------------------------|")
             print ("")

        
        

    elif (key == '3'):
        print("|----------------------Menu de Produtos-------------------------|")
        print("1-Create Produto")
        print("2-Read Produto")
        print("3-Update Produto")
        print("4-Delete Produto")
        print("|---------------------------------------------------------------|")
        sub = input("Digite a opção desejada? (V para voltar) ")
        print ("")      

        if (sub == '1'):
            print("|-------------------Criação de Produto-------------------------|")
            criar_produto(session)
            print ("")

        elif (sub == '2'):
            print("|----------------Listagem de Produto-------------------------|")
            listar_produtos(session)
            print ("")
        
        elif (sub == '3'):
            print("|--------------------------------------------------------------|")
            editar_produto(session)
            print ("")
        
        elif (sub == '4'):
            print("|--------------------------------------------------------------|")
            deletar_produto(session)
            print ("")
            

session.shutdown()
print("Vlw Flw...")