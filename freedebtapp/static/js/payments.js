    $(function() {
    $('button#proceed').bind('click', function(){
    var amount = $('#amountpaid').val();
      $.getJSON($SCRIPT_ROOT+'/paymentsAjax',{amt:amount}, function(data){
          console.log(data);
          console.log("Hello");
          $("#proceed").remove();
          $("#addmore").append('<div id="changeViewer"><h2 class="subtitle">Do you wish to save</h2><h2 id="quantumVal"></h2>');
          $("#quantumVal").append(data['quantum']);
          $("#addmore").append('<div class="field is-grouped"><p class="control"><button id="acceptQuantum" class="button is-rounded">Accept</button></p><p class="control"><button id="declineQuantum" class="button is-danger is-rounded">Decline</button></p></div>')
          $('button#acceptQuantum').bind('click', function(){
            console.log("Accepted");
            console.log(data['quantum']);
            var acceptMessage = 'You have accepted ' + data['quantum'];
            $.getJSON($SCRIPT_ROOT+'/acceptQuantum',{bal: data['quantum']}, function(data){
                $("#addmore").empty();
                $("#postTransactionMessage").append(acceptMessage);
                $("#addmore").append('<button id="finalPay" class="button is-link is-inverted is-outlined">Make Payment</button>');
                $('button#finalPay').bind('click', function(){
                   console.log("PaymentCompleteClicked");
                   $.getJSON($SCRIPT_ROOT+'/acceptPayment', {pay_amt: amount},function(data){
                        console.log("Completed Payment Cycle");
                        location.reload();
                   });
                });
            });
           });
           $('button#declineQuantum').bind('click', function(){
            console.log("Declined");
            console.log(data['quantum']);
            var rejectMessage = 'You have rejected ' + data['quantum'];
            $.getJSON($SCRIPT_ROOT+'/acceptQuantum',{bal: 0.0}, function(data){

                $("#addmore").empty();
                $("#postTransactionMessage").append(rejectMessage);
                $("#addmore").append('<button id="finalPay" class="button is-link is-inverted is-outlined">Make Payment</button>');
                $('button#finalPay').bind('click', function(){
                   console.log("PaymentCompleteClicked");
                   $.getJSON($SCRIPT_ROOT+'/acceptPayment', {pay_amt: amount},function(data){
                        console.log("Completed Payment Cycle");
                        location.reload();
                   });
                });
            });
           });


        });
        return false;
      });
    });
