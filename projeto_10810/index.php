<!DOCTYPE html>
<html lang="pt-pt">
<head>
    <meta charset="UTF-8">
    <title>UFCD 10810 Fundamentos do desenvolvimento de modelos analíticos em Python</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="estilos.css">
</head>
<body>
    <?php
        $txt = 'resumo/';
        $img = 'imagens/';
        $err = 'erros.txt';
        $erros = $txt.$err;
    ?>

<div class="container py-5">

    <!-- Texto -->
    <section class="mb-5">
        <h3 class="mb-5">10810 Fundamentos do desenvolvimento de modelos analíticos em Python</h3>

        <div class="row">
            <div class="col-md-12 mb-4">
                <h5 class="mb-4">Listagem de Erros</h5>
                <p>
                <?php
                if(file_exists($erros)){
                    $arquivo = fopen ($erros, 'r');
                    while(!feof($arquivo)) print nl2br(fgets($arquivo));
                    fclose($arquivo);
                }
                ?>
                </p>
                <br><hr>
            </div>
        </div>

        <div class="row">
            <h4 class="mb-4">Estatísticas</h4>
            <?php
                $arquivos = scandir($txt);

                $lista[] = array();
                foreach ($arquivos as $arq) {
                if (strlen($arq) >= 5 and $arq != $err) {
                        $lista[] = $arq;
                    }
                }

                if(count($lista)>0){
                    for($i=0; $i<count($lista); $i++){
                        if(!empty($lista[$i])){
                            $nome = '';
                            $temp = explode('.', $lista[$i]);
                            if(isset($temp[0])) $nome = str_replace('_',' ',$temp[0]);
                           
                            print '<div class="col-md-6 mb-3">';
                                print '<div class="caixa">';
                                    print '<h5>Arquivo: '. $nome .'</h5>';
                                    
                                    print '<p>';
                                        $arquivo = fopen ($txt.$lista[$i], 'r');
                                        print '<table>';
                                        $m = 0;
                                        while(!feof($arquivo)){
                                            
                                            print '<tr>';
                                                $texto = trim(fgets($arquivo));
                                                
                                                for($j=0; $j<strlen($texto); $j++) $texto = str_replace('  ', ' ', $texto);
                                                
                                                $colunas = explode(' ', $texto);

                                                if($m==0) $ncolunas = count($colunas);
                                                
                                                for($k=0; $k<$ncolunas; $k++){
                                                    if(isset($colunas[$k])) print '<td class="c">'. $colunas[$k] .'</td>';
                                                }

                                            print '</tr>';
                                            $m++;
                                        }
                                        print '</table>';
                                        fclose($arquivo);
                                    print '</p>';
                                    
                                print '</div>';
                            print '</div>';
                        }
                    }
                }

            ?>
            <hr>
        </div>
    </section>

    <!-- Galeria de gráficos -->
    <section>
        
        <h4 class="mb-4">Gráficos</h4>
        
        <div class="row g-3 gallery">
            <?php
                $arquivos = scandir($img);

                $k = 0;
                $lista[] = array();
                foreach ($arquivos as $arq) {
                if (strlen($arq) >= 5) {
                    $temp = explode('.', $arq);
                        if(end($temp) == 'jpg'){
                            print '<div class="col-6 col-md-4"><img src="'.$img.$arq.'" class="img-fluid rounded gallery-item" data-index="'. $k++ .'"></div>';
                        }
                    }
                }
            ?>
        </div>

    </section>
    
</div>

<footer class="bg-dark text-light mt-5 x-100">
    <div class="container py-4">

        <div class="row">
            <div class="col-md-6 mb-3 mb-md-0">&nbsp;
                
            </div>

            <div class="col-md-6 text-md-end"><p class="mb-0 small">© 2026 Técnico/a Especialista em Gestão de Informação e Ciência de Dados</p></div>
        </div>
    </div>
</footer>


<!-- Modal -->
<div class="modal fade" id="imageModal" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content position-relative">
            <button class="modal-nav modal-prev" id="prevBtn">‹</button>
            <button class="modal-nav modal-next" id="nextBtn">›</button>
            <div class="modal-body p-0 text-center">
                <img id="modalImage" class="img-fluid w-100" alt="">
            </div>
        </div>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>

<script>
  const images = document.querySelectorAll('.gallery-item');
  const modalImage = document.getElementById('modalImage');
  const modal = new bootstrap.Modal(document.getElementById('imageModal'));
  let currentIndex = 0;

  images.forEach(img => {
    img.addEventListener('click', () => {
      currentIndex = parseInt(img.dataset.index);
      showImage();
      modal.show();
    });
  });

  function showImage() {
    modalImage.src = images[currentIndex].src;
  }

  document.getElementById('prevBtn').addEventListener('click', () => {
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    showImage();
  });

  document.getElementById('nextBtn').addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % images.length;
    showImage();
  });
</script>

</body>
</html>