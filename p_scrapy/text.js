
var page = require('webpage').create(), //��ȡ����dom��web��ҳ�Ķ���
system = require('system'),         //��ȡ����ϵͳ����
address;
console.log("sssss");
if (system.args.length === 1) {
    phantom.exit(1);
} else {
    address = system.args[1];

    page.open(address, function (status) {   //����url
        console.log(page.content);
        phantom.exit();
    });
};