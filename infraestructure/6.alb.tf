
resource "aws_lb" "api_alb" {
    name = "${var.project_name}-api-alb"
    internal = false
    security_groups = [aws_security_group.api_alb_sg.id]
    subnets = module.vpc.public_subnets
}

resource "aws_lb_target_group" "api_target_group" {
    depends_on = [ module.vpc ]

    name = "${var.project_name}-api-target-group"
    port = 80
    protocol = "HTTP"
    target_type = "ip"
    vpc_id = module.vpc.vpc_id
    deregistration_delay =  10

    health_check {
        path = "/health-check"
        interval = 10
        timeout = 5
        healthy_threshold = 2
        unhealthy_threshold = 2
        matcher = 200
    }
}

resource "aws_lb_listener" "api_alb_listener" {
    load_balancer_arn = "${aws_lb.api_alb.arn}"
    port = 80
    protocol = "HTTP"

    default_action {
        type = "forward"
        target_group_arn = aws_lb_target_group.api_target_group.arn
    }
}

resource "aws_security_group" "api_alb_sg" {
    name = "${var.project_name}-api-alb-sg"
    description = "Allow traffic from internet"
    vpc_id = module.vpc.vpc_id

    ingress = [
        {
            description = "Allow traffic from internet"
            from_port = 80
            to_port = 80
            protocol = "tcp"
            cidr_blocks = ["0.0.0.0/0"]
            ipv6_cidr_blocks = []
            prefix_list_ids = []
            security_groups = []
            self = false
        }
    ]

    egress = [
        {
            description = "Allow all outbound traffic"
            from_port = 0
            to_port = 0
            protocol = "-1"
            cidr_blocks = ["0.0.0.0/0"]
            ipv6_cidr_blocks = []
            prefix_list_ids = []
            security_groups = []
            self = false
        }
    ]

    tags = {
        Name = "${var.project_name}-api-alb-sg"
        Owner: "Gabriel",
		Project: "${var.project_name}",
		Environment: "${var.environment}"
    }
}

output "api_target_group-arn" {
    value = aws_lb_target_group.api_target_group.arn
}

output "api_dns" {
    value = aws_lb.api_alb.dns_name
}