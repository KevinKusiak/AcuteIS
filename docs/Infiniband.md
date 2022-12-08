Infiniband (CCN type infrastructure)
====================================

- Atomic computations on InfiniBand packets flowing through the switches
- Uses HCAs, switches to processors nodes, and user consoles
- Node layer, physical layer
- Switch: follows node layers, and tops off with a packet relay
- Independent virtual lanes provide for lossless fabric (flow control) and VL arbitration for QoS
- Network layer: utilizes GID addressing which is based on IPv6 addressing scheme
- Network layer is used for multicast distribution within end nodes, and enables for routing between IB subnets
- Transport layer uses QP (as transport endpoints) in asynchronous interfaces (send/receive/completion queues), full transport offloads(segmentation, reassembly, timers, retransmission), and send/receives, and atomics
- Kernel bypass in the transport layer allows for lower latency and CPU offloads, and is enabled through QPs, CQs(completion queues), PDs(protection domains), or MRs(memory regions)
- Is partitioned similarly to FC Zoning
- Uses subnet manager model to administer a fabric topology, and is usually implemented at end nodes or switches
- Subnet administration provides path records and QoS management.
- ULPs connect InfiniBand to common interfaces
- With clustering in ULPs, uses MPI (message passing interface), and RDS (reliable datagram socket)
- With the network in ULPs, uses IPoIB (IP over InfiniBand), and SDP (socket direct protocol)
- With storage in ULPs, uses SRP (SCSI RDMA protocol), iSER (iSCSI extensions for RDMA), and NFSoRDMA (NFS over RDMA)
- iSER leverages all iSCSI infrastructure, whilst using IP of InfiniBand
- NFS over RDMA is defined by IETF, with ONC-RPC extensions for RDMA, and with NFS mapping
- Input output consolidation has a high bandwidth pipe for capacity provisioning, dedicated I/O channels which enable convergence, and gateways which all independently share remote fibre channel and ethernet ports

STATS
=====

- (Block Storage) I/O Read: 1.4 Gb/s
- (Block Storage) I/O Write: 1.2 Gb/s
- (File Storage)      Read: 1.d3 Gb/s
- (File Storage)      Write: 0.59 Gb/s
- (Clustering (MPI))  Latency: 1.2 us
- (Clustering(MPI))   Message rate: 30M msg/sec
- (Latency)           RDMA Read: 1.87 us (roundtrip)
- (Latency)           RDMA Write: 0.99 us
- (Bandwidth)         Unidirectional: 1.5 - 1.9 Gb/s
- (Bandwidth)         Bidirectional: 3.0 - 3.4 Gb/s