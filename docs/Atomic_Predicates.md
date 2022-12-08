Atomic Predicates
=================

- Do verify data planes, we need a graph where each node is a packet filter or a packet transformer
- We can custom design data structures and algorithms to directly compute reachability trees (header space analysis/hassel in C, or the atomic predicates verifier)
- There are 2 methods of computing packet sets that can travel from port x to port y: forward reachability trees rooted at a source port, and reverse reachability trees routed at a destination port
- The reachability set along multiple paths is the union of reachability sets along individual paths
- Considering both the intersection and union of packet sets, multidimensional sets can have any set number of allowed interval in each dimension and arbitrary overlaps, and additionally the worst case computation time of set intersection/union is 0(2^h)
- Time and space performance of a network verification tool depends on data structure for representing packet sets, and the algorithm for computing reachability sets
- In an atomic predicament model, each access control list (ACL) is essentially being converted into an AP by specifying the packet set allowed by the ACL (box model)
- In this box model, each AP is computed from the forwarding table (FIB)
- Each variable in an AP represents an individual packet header arbitrary
- Increasing the # of rules in an ACL or an FIB does not always mean extra BDD nodes
- AP computation time is affected by the arbitrary order of predicates (usually in fractions of seconds)
- The set of packets P that can pass through an output port is specified by the conjunction of its predicates for forwarding and ACLs (which is ultimately represented by 2 sets of identifiers of atomic predicates)
- Reachability tree has every path along which a nonempty set of packets can travel from source port to another port in the network, ultimately being classified as nodes
- A black hole in the FIB is a set of packets that is being dropped due to no entry being recorded in the FIB
- A slice is a set of ports together with a set of packets allowed in the slice
- A source port can traverse the reachability tree from source port s to check that every path in the tree passes through an input port of the waypoint before reaching any destination port in the specified set
- In this case, every single packet that is encapsulated in port s pass through any member of a set of waypoints or several waypoints in a specified sequence

BENEFITS:
- Specify coarsest equivalence classes of packets
- An atomic predicate essentially represents a very large number of equivalent packets in numerous fragments of the packet space
- Conjunction of disjunction of two separate predicates is computed as the union of 2 distinct sets of integers

THEOREMS:
1.  If the length of a packet header is h bits, and an ACL rule specifies each header field by an interval, a prefix or a suffix, then the number of nodes in the BDD graph representing an ACL rule is less or equal to 2+2h (h being the number of header bits relevant for verification)
2.  For a given set P of predicates, the atomic predicates for set P specify the equivalence classes in the set of all packets with respect to P
3.  The set of atomic predicates for the union of set P1 and set P2 is {ai, ..., ak} where, for i in the set of {1, ..., k}, ai is computed by the computation formula

Networks with Packet Transformers:
- Letting U denote the set of all elements, without qualification, an element x is always in set U, and  a set of elements is always a subset of U. A predicate specifies a set of elements in U. Predicate true specifies U. Predicate false specifies the empty set

Transformers:
- Letting T denote a set of transformers, a transformer T in the set of predefined T is able to map an element from its domain to a set of elements in its range. Both the domain and the range of T are subsets of U. For a transformer T, and an element x in the domain of T, T(x) can denote the set of elements after transformation.
- T(D) = (x in the set of D), T(x)

PROOF:
Given a set P of predicates its set {p1, ..., pk} of APs satisfies:
1.  p1 is not false, and the set of Ai is, in first order logic, from {1, ..., k}.
2.  Vpi = true
3.  pi ^ pj = false, for i is not j
4.  Each predicate P in set P, predicate P is not false, and is equal to the disjunction of a subset of atomic predicates.
5.  k is the min number such that the set {pi, ..., pk} satisfies each of the previous 4 properties.

COMPUTATION FORMULA:
{ai = bi ^ di2 | ai is not false, i1 is in the set of {1, ..., l}, i2 is in the set of {1, ..., m}}