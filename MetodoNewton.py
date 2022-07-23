from inspect import signature
import numpy as np
import seaborn
import matplotlib as mpl
class NewtonsMethod():
  """
  Classe que estima o valor de uma raíz de um Polinômio
  de grau 'N' e possui métodos de visualização do polinômio e
  das raíz estimada.
  """
  
  def __init__(self,Px):
    '''
    Inicializa uma instância da classe NewtonsMethod a partir de uma função
    fornecida como argumento para o parâmetro Px.
    '''
    #Checando se a função fornecido como argumento para o parâmetro Px é valida.
    if not callable(Px):
      raise ValueError(f'''
      Argumento fornecido para parâmetro Px não é do tipo função,
      mas sim do tipo: {type(Px)}
      ''') 
    if len(signature(Px).parameters)!=1:
      raise ValueError(f'''
      Função Fornecida Para o Polinômio 'Px' deve conter apenas 1 parametro
      chamado 'x', mas a função fornecida possui {len(signature(Px).parameters)}
      parâmetros de nomes: {list(signature(Px).paramenters.keys())}
      ''')
    try:
      out=Px(np.random.randn())
      if type(out)!=int and type(out)!=float:
        raise ValueError(f''' 
        Valor de Retorno da função Px deve ser do tipo 'int', ou
        do tipo 'float', mas o valor de retorno da função fornecida
        é {type(out)}
                ''')
    except TypeError:
      raise ValueError('''
      Ocorreu um erro de tipo ao fornecer um 'float' como argumento para o
      parâmetro 'x' da função, cheque a função fornecida
      ''')
    except:
      raise ValueError('''Ocorreu um erro não identificado ao fornecer um 'float' como
      argumento para o parâmetro 'x' da função, cheque a função Px fornecida''')
      
    #Armazenando a função como atributo e vetorizando-a utilizando o numpy caso 
    #seja válida.
    
    self.Px=Px
    self.vect_Px=np.vectorize(Px,otypes=['float64'])
    self.raiz_aprox=None
    
  def dPx(self,x):
    '''
    Método utilizado para calcular a derivada do polinômio Px em um ponto
    arbitrário x, utilizando a fórmula do coef. angular da reta secante
    com a diferença entre os valores de x dos pontos desta (h) igual a
    0.0001, para aproximar o coef.angular da reta tangente.
    '''
    return (self.Px(x+0.0001)-self.Px(x))/0.0001
  
  def encontrar_raiz(self,it=1000):
    '''
    Método utilizado para implementar o Algoritmo de Newton para aproximação
    de uma raiz real de um polinômio Px de grau 'N'.
    It:Número de Iterações do Algoritmo que serão realizadas.
    '''
    r0=np.random.randn()
    for i in range(it):
      try:
        passo=-(self.Px(r0)/self.dPx(r0))
      except ZeroDivisionError:
        break
      r0+=passo
    self.raiz_aprox=r0
    return r0
  
  def plotar_polinomio(self,raiz_aprox=False,raiz_real=None,xmax=50,xmin=-50,step=0.1):
    '''
    Método Utilizado para fazer um gráfico do polinômio utilzando as bibliotecas
    matplotlib e seaborn para um conjunto aleatório de valores 'x'.

    raiz_aprox: Valor booleano, verdadeiro caso deseja-se plotar a raiz
    aproximada encontrada pelo algoritmo de newton (Caso não tenha sido
    executdo ainda retorna um erro), caso contrário plota a origem do gráfico.

    raiz_real: Float ou Int, Opção de se fornecer uma raiz real do polinômio
    para plotagem e comparação. Caso não seja do tipo 'int' ou 'float' retorna
    um erro.
    
    xmax: Valor Máximo De 'x' para plotar
    xmin: Valor Mínimo de 'x' para plotar
    step: Distância entre valores a serem plotados.
    '''
    
    if raiz_aprox==True:
      if self.raiz_aprox is None:
        raise ValueError('''
        O valor da raiz aproximada ainda não foi encontrado, execute o  método
        'encontrar_raiz' previamente.
        ''')
      raprox=self.raiz_aprox
    elif raiz_aprox is None or raiz_aprox==False:
      raprox=None
      
    elif type(raiz_aprox) is not bool:
      raise ValueError(f'''
      Argumento passado para parâmetro raiz_aprox deve ser
      True ou False, porém foi passado {type(raiz_aprox)}
      ''')

    if raiz_real is None:
      rreal=None
      
    elif type(raiz_real)!=int and type(raiz_real)!=float:
      raise ValueError(f'''
      Argumento passado para parâmetro raiz real deve ser do tipo 'int' ou
      'float', porém foi passado tipo: {type(raiz_real)}
      ''')
    else:
      rreal=raiz_real
    
    X=np.arange(xmin,xmax,step)
    y=self.vect_Px(X)
    seaborn.set_theme(context='notebook',style='darkgrid',palette='pastel',
                      font='Monospace',font_scale=1.3)
    fig,ax=mpl.pyplot.subplots(figsize=(12,8))
    ax.plot(X,y,linewidth=2,color='red',label='P(x)')
    if raprox is not None:
      ax.plot(raprox,self.Px(raprox),marker='o',color='blue',label='Raiz Aproximada')
    if rreal is not None:
      ax.plot(rreal,self.Px(rreal), marker='o',color='green',label='Raiz Real')
    ax.legend()
    return (fig,ax)
    
